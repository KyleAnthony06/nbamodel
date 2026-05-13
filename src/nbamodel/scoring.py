from __future__ import annotations

from pathlib import Path
from typing import Any

from nbamodel.csv_io import Row, read_csv, write_csv
from nbamodel.learning import adjustment_for_pick, load_history_adjustments
from nbamodel.math_utils import (
    american_implied_probability,
    as_bool,
    as_float,
    clamp,
    normalize,
)


PICK_FIELDS = [
    "date",
    "pick_type",
    "rank",
    "confidence_score",
    "team",
    "opponent",
    "game_id",
    "player",
    "market",
    "side",
    "line",
    "american_odds",
    "book",
    "projected_value",
    "edge",
    "edge_pct",
    "feature_score",
    "learning_adjustment",
    "top_factors",
    "risk_flags",
    "notes",
]


def _direction(row: Row) -> int:
    return -1 if row.get("side", "").strip().lower() == "under" else 1


def _weighted_score(features: dict[str, float], weights: dict[str, float]) -> float:
    total_weight = sum(abs(weight) for weight in weights.values())
    if total_weight == 0:
        return 0.0
    return sum(features.get(name, 0.0) * weight for name, weight in weights.items()) / total_weight


def _confidence_from_feature_score(feature_score: float) -> float:
    return clamp(50.0 + (feature_score * 35.0), 1.0, 99.0)


def _format_factors(features: dict[str, float], weights: dict[str, float], limit: int = 5) -> str:
    contributions = [
        (name, features.get(name, 0.0) * weight)
        for name, weight in weights.items()
        if abs(features.get(name, 0.0) * weight) >= 0.01
    ]
    contributions.sort(key=lambda item: abs(item[1]), reverse=True)
    return "; ".join(f"{name}={value:+.2f}" for name, value in contributions[:limit])


def _risk_flags(row: Row) -> str:
    flags: list[str] = []
    if as_float(row.get("news_risk")) >= 0.6:
        flags.append("news risk")
    if as_bool(row.get("is_back_to_back")):
        flags.append("back-to-back")
    if as_float(row.get("projected_minutes")) < 24 and row.get("pick_type") != "spread":
        flags.append("low minutes")
    if as_float(row.get("shot_volume_stability")) < 0.45 and row.get("market", "").lower() != "spread":
        flags.append("volatile volume")
    return "; ".join(flags)


def _price_feature(american_odds: float) -> float:
    implied = american_implied_probability(american_odds)
    # Prefer reasonably priced bets. Large juice lowers the score, plus-money is
    # slightly positive but never enough to overcome a poor projection.
    return clamp((0.57 - implied) / 0.18, -1.0, 1.0)


def score_prop(row: Row, weights: dict[str, float]) -> Row:
    direction = _direction(row)
    line = as_float(row.get("line"))
    projection = as_float(row.get("projected_value"))
    edge = (projection - line) * direction
    edge_pct = edge / max(abs(line), 1.0)
    recent_edge = (as_float(row.get("last_5_avg")) - line) * direction / max(abs(line), 1.0)
    trend_edge = (
        as_float(row.get("last_5_avg")) - as_float(row.get("season_avg"))
    ) * direction / max(abs(line), 1.0)
    attempt_trend = (
        as_float(row.get("last_5_attempts")) - as_float(row.get("season_attempts"))
    ) * direction / max(abs(as_float(row.get("season_attempts"))), 1.0)
    opponent_rank = as_float(row.get("opp_rank_vs_market"), 15.5)
    matchup = ((opponent_rank - 15.5) / 14.5) * direction
    defense_rating_edge = normalize((as_float(row.get("opp_def_rating"), 115.0) - 115.0) * direction, 8.0)
    usage_bump = normalize(as_float(row.get("injury_usage_bump")) * direction, 6.0)
    minutes = normalize(as_float(row.get("projected_minutes")) - as_float(row.get("minutes_floor"), 24.0), 12.0)
    rest = normalize(as_float(row.get("rest_days"), 1.0) - 1.0, 2.0)
    if as_bool(row.get("is_back_to_back")):
        rest -= 0.35

    features = {
        "projection_edge": normalize(edge_pct, 0.18),
        "recent_form": normalize(recent_edge, 0.20),
        "trend": normalize(trend_edge, 0.18),
        "attempt_trend": normalize(attempt_trend, 0.35),
        "matchup": clamp(matchup, -1.0, 1.0),
        "defense_rating": defense_rating_edge,
        "injury_usage": usage_bump,
        "minutes_security": minutes,
        "shot_quality": normalize(as_float(row.get("shot_quality"), 0.5) - 0.5, 0.35),
        "volume_stability": normalize(as_float(row.get("shot_volume_stability"), 0.5) - 0.5, 0.35),
        "team_total": normalize((as_float(row.get("team_total")) - 112.0) * direction, 12.0),
        "pace": normalize((as_float(row.get("pace"), 99.0) - 99.0) * direction, 7.0),
        "rest": clamp(rest, -1.0, 1.0),
        "price": _price_feature(as_float(row.get("american_odds"))),
        "news_risk": -clamp(as_float(row.get("news_risk")), 0.0, 1.0),
    }
    feature_score = _weighted_score(features, weights)
    output = dict(row)
    output.update(
        {
            "pick_type": "prop",
            "edge": f"{edge:.2f}",
            "edge_pct": f"{edge_pct:.3f}",
            "feature_score": f"{feature_score:.3f}",
            "top_factors": _format_factors(features, weights),
        }
    )
    output["risk_flags"] = _risk_flags(output)
    return output


def score_spread(row: Row, weights: dict[str, float]) -> Row:
    line = as_float(row.get("line"))
    projected_margin = as_float(row.get("projected_margin"))
    market_consensus = as_float(row.get("market_consensus"), line)
    opening_line = as_float(row.get("opening_line"), line)
    current_line = as_float(row.get("current_line"), line)
    edge = projected_margin + line
    movement = opening_line - current_line
    consensus_edge = market_consensus + line

    features = {
        "projection_edge": normalize(edge, 7.0),
        "power_rating": normalize(
            as_float(row.get("team_power_rating")) - as_float(row.get("opponent_power_rating")),
            8.0,
        ),
        "injury_net_rating": normalize(as_float(row.get("injury_net_rating")), 6.0),
        "rest_advantage": normalize(as_float(row.get("rest_advantage")), 2.0),
        "schedule_spot": normalize(as_float(row.get("schedule_spot")), 2.0),
        "market_movement": normalize(movement, 3.0),
        "consensus_edge": normalize(consensus_edge, 4.0),
        "pace_edge": normalize(as_float(row.get("pace_edge")), 4.0),
        "rebounding_edge": normalize(as_float(row.get("rebounding_edge")), 5.0),
        "turnover_edge": normalize(as_float(row.get("turnover_edge")), 4.0),
        "clutch_edge": normalize(as_float(row.get("clutch_edge")), 5.0),
        "motivation": normalize(as_float(row.get("motivation")), 2.0),
        "price": _price_feature(as_float(row.get("american_odds"))),
        "news_risk": -clamp(as_float(row.get("news_risk")), 0.0, 1.0),
    }
    feature_score = _weighted_score(features, weights)
    output = dict(row)
    output.update(
        {
            "pick_type": "spread",
            "player": "",
            "market": "spread",
            "side": "team",
            "projected_value": f"{projected_margin:.2f}",
            "edge": f"{edge:.2f}",
            "edge_pct": f"{edge / max(abs(line), 1.0):.3f}",
            "feature_score": f"{feature_score:.3f}",
            "top_factors": _format_factors(features, weights),
        }
    )
    output["risk_flags"] = _risk_flags(output)
    return output


def rank_picks(
    date: str,
    props_path: Path,
    spreads_path: Path,
    output_dir: Path,
    config: dict[str, Any],
) -> tuple[Path, list[Row]]:
    props = read_csv(props_path)
    spreads = read_csv(spreads_path)
    learning_config = config.get("learning", {})
    history_path = Path(learning_config.get("history_path", "data/history/pick_history.csv"))
    adjustments = load_history_adjustments(
        history_path=history_path,
        max_adjustment=float(learning_config.get("max_adjustment", 5.0)),
        min_sample=int(learning_config.get("min_sample", 20)),
    )

    scored_props = [score_prop(row, config["prop_weights"]) for row in props]
    scored_spreads = [score_spread(row, config["spread_weights"]) for row in spreads]

    for row in scored_props + scored_spreads:
        row["date"] = row.get("date") or date
        adjustment = adjustment_for_pick(row, adjustments)
        score = _confidence_from_feature_score(as_float(row.get("feature_score"))) + adjustment
        row["learning_adjustment"] = f"{adjustment:.2f}"
        row["confidence_score"] = f"{clamp(score, 1.0, 99.0):.2f}"

    scored_props.sort(key=lambda item: as_float(item["confidence_score"]), reverse=True)
    scored_spreads.sort(key=lambda item: as_float(item["confidence_score"]), reverse=True)

    final_rows: list[Row] = []
    for rank, row in enumerate(scored_props[:5], start=1):
        row["rank"] = str(rank)
        final_rows.append(row)
    if scored_spreads:
        top_spread = scored_spreads[0]
        top_spread["rank"] = "1"
        final_rows.append(top_spread)

    output_path = output_dir / f"picks_{date}.csv"
    write_csv(output_path, final_rows, PICK_FIELDS)
    return output_path, final_rows

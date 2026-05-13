from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nbamodel.csv_io import Row, read_csv, write_csv
from nbamodel.learning import rebuild_summary
from nbamodel.math_utils import as_float
from nbamodel.scoring import PICK_FIELDS


GRADE_FIELDS = PICK_FIELDS + [
    "actual_value",
    "team_score",
    "opponent_score",
    "result",
    "result_margin",
    "graded_at",
]


def _prop_key(row: Row) -> tuple[str, str, str, str]:
    return (
        row.get("date", "").strip(),
        row.get("player", "").strip().lower(),
        row.get("team", "").strip().lower(),
        row.get("market", "").strip().lower(),
    )


def _spread_key(row: Row) -> tuple[str, str, str]:
    return (
        row.get("date", "").strip(),
        row.get("game_id", "").strip().lower(),
        row.get("team", "").strip().lower(),
    )


def _settle_prop(pick: Row, actual: float) -> tuple[str, float]:
    line = as_float(pick.get("line"))
    margin = actual - line
    if pick.get("side", "").lower() == "under":
        margin = line - actual
    if margin > 0:
        return "win", margin
    if margin < 0:
        return "loss", margin
    return "push", 0.0


def _settle_spread(pick: Row, team_score: float, opponent_score: float) -> tuple[str, float]:
    margin = team_score - opponent_score + as_float(pick.get("line"))
    if margin > 0:
        return "win", margin
    if margin < 0:
        return "loss", margin
    return "push", 0.0


def grade_picks(
    date: str,
    picks_path: Path,
    prop_actuals_path: Path,
    spread_actuals_path: Path,
    output_dir: Path,
    config: dict[str, Any],
) -> tuple[Path, Path, list[Row]]:
    picks = read_csv(picks_path)
    prop_actuals = {_prop_key(row): row for row in read_csv(prop_actuals_path)}
    spread_actuals = {_spread_key(row): row for row in read_csv(spread_actuals_path)}
    graded_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    graded: list[Row] = []

    for pick in picks:
        row = dict(pick)
        pick_type = row.get("pick_type", "").lower()
        if pick_type == "prop":
            actual = prop_actuals.get(_prop_key(row))
            if actual is None:
                row.update({"result": "missing", "graded_at": graded_at})
            else:
                actual_value = as_float(actual.get("actual_value"))
                result, margin = _settle_prop(row, actual_value)
                row.update(
                    {
                        "actual_value": f"{actual_value:.2f}",
                        "result": result,
                        "result_margin": f"{margin:.2f}",
                        "graded_at": graded_at,
                    }
                )
        elif pick_type == "spread":
            actual = spread_actuals.get(_spread_key(row))
            if actual is None:
                row.update({"result": "missing", "graded_at": graded_at})
            else:
                team_score = as_float(actual.get("team_score"))
                opponent_score = as_float(actual.get("opponent_score"))
                result, margin = _settle_spread(row, team_score, opponent_score)
                row.update(
                    {
                        "actual_value": f"{team_score - opponent_score:.2f}",
                        "team_score": f"{team_score:.0f}",
                        "opponent_score": f"{opponent_score:.0f}",
                        "result": result,
                        "result_margin": f"{margin:.2f}",
                        "graded_at": graded_at,
                    }
                )
        else:
            row.update({"result": "unknown_pick_type", "graded_at": graded_at})
        graded.append(row)

    graded_path = output_dir / f"graded_picks_{date}.csv"
    write_csv(graded_path, graded, GRADE_FIELDS)

    learning_config = config.get("learning", {})
    history_path = Path(learning_config.get("history_path", "data/history/pick_history.csv"))
    existing_history = [
        row
        for row in read_csv(history_path)
        if row.get("date") != date
        or row.get("result", "").lower() not in {"win", "loss", "push", "missing"}
    ]
    write_csv(history_path, existing_history + graded, GRADE_FIELDS)

    summary_path = Path(learning_config.get("summary_path", "data/history/model_summary.csv"))
    rebuild_summary(
        history_path=history_path,
        summary_path=summary_path,
        max_adjustment=float(learning_config.get("max_adjustment", 5.0)),
        min_sample=int(learning_config.get("min_sample", 20)),
    )
    return graded_path, summary_path, graded

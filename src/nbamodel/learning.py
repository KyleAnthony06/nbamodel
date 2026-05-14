from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import mean

from nbamodel.csv_io import Row, read_csv, write_csv
from nbamodel.math_utils import as_float, clamp


SUMMARY_FIELDS = [
    "segment_type",
    "segment",
    "sample_size",
    "wins",
    "losses",
    "pushes",
    "win_rate",
    "avg_confidence",
    "calibration_adjustment",
]


def _result_value(row: Row) -> int | None:
    result = row.get("result", "").lower()
    if result == "win":
        return 1
    if result == "loss":
        return 0
    return None


def _adjustment(rows: list[Row], max_adjustment: float, min_sample: int) -> float:
    graded = [value for row in rows if (value := _result_value(row)) is not None]
    if len(graded) < min_sample:
        return 0.0

    # A 52.4% break-even target approximates -110 pricing. The adjustment is
    # intentionally small so noisy history nudges rankings instead of driving them.
    win_rate = mean(graded)
    return clamp((win_rate - 0.524) * 30.0, -max_adjustment, max_adjustment)


def load_history_adjustments(
    history_path: Path,
    max_adjustment: float,
    min_sample: int,
) -> dict[str, float]:
    rows = read_csv(history_path)
    grouped: dict[str, list[Row]] = defaultdict(list)
    for row in rows:
        pick_type = row.get("pick_type", "").lower()
        market = row.get("market", "").lower()
        side = row.get("side", "").lower()
        if pick_type:
            grouped[f"type:{pick_type}"].append(row)
        if market:
            grouped[f"market:{market}"].append(row)
        if pick_type and market:
            grouped[f"type_market:{pick_type}:{market}"].append(row)
        if market and side:
            grouped[f"market_side:{market}:{side}"].append(row)

    return {
        segment: _adjustment(segment_rows, max_adjustment, min_sample)
        for segment, segment_rows in grouped.items()
    }


def adjustment_for_pick(row: Row, adjustments: dict[str, float]) -> float:
    pick_type = row.get("pick_type", "").lower()
    market = row.get("market", "").lower()
    side = row.get("side", "").lower()
    keys = [
        f"type:{pick_type}",
        f"market:{market}",
        f"type_market:{pick_type}:{market}",
        f"market_side:{market}:{side}",
    ]
    return sum(adjustments.get(key, 0.0) for key in keys)


def rebuild_summary(
    history_path: Path,
    summary_path: Path,
    max_adjustment: float,
    min_sample: int,
) -> list[Row]:
    history = read_csv(history_path)
    grouped: dict[tuple[str, str], list[Row]] = defaultdict(list)

    for row in history:
        pick_type = row.get("pick_type", "").lower()
        market = row.get("market", "").lower()
        side = row.get("side", "").lower()
        if pick_type:
            grouped[("type", pick_type)].append(row)
        if market:
            grouped[("market", market)].append(row)
        if market and side:
            grouped[("market_side", f"{market}:{side}")].append(row)

    summary: list[Row] = []
    for (segment_type, segment), rows in sorted(grouped.items()):
        wins = sum(1 for row in rows if row.get("result", "").lower() == "win")
        losses = sum(1 for row in rows if row.get("result", "").lower() == "loss")
        pushes = sum(1 for row in rows if row.get("result", "").lower() == "push")
        decisions = wins + losses
        avg_confidence = mean(as_float(row.get("confidence_score")) for row in rows)
        adjustment = _adjustment(rows, max_adjustment, min_sample)
        summary.append(
            {
                "segment_type": segment_type,
                "segment": segment,
                "sample_size": str(len(rows)),
                "wins": str(wins),
                "losses": str(losses),
                "pushes": str(pushes),
                "win_rate": f"{(wins / decisions) if decisions else 0.0:.3f}",
                "avg_confidence": f"{avg_confidence:.2f}",
                "calibration_adjustment": f"{adjustment:.2f}",
            }
        )

    write_csv(summary_path, summary, SUMMARY_FIELDS)
    return summary

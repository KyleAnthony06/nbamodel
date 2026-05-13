from __future__ import annotations

from pathlib import Path

from nbamodel.csv_io import Row, read_csv


def _escape(value: object) -> str:
    text = str(value or "").replace("\n", " ").strip()
    return text.replace("|", "\\|")


def _pick_text(row: Row) -> str:
    pick_type = row.get("pick_type", "").lower()
    if pick_type == "spread":
        return f"{row.get('team', '')} {row.get('line', '')}"

    player = row.get("player", "")
    market = row.get("market", "")
    side = row.get("side", "").upper()
    line = row.get("line", "")
    return f"{player} {side} {line} {market}"


def _game_text(row: Row) -> str:
    team = row.get("team", "")
    opponent = row.get("opponent", "")
    game_id = row.get("game_id", "")
    if game_id:
        return f"{team} vs {opponent} ({game_id})"
    return f"{team} vs {opponent}"


def _result_text(row: Row) -> str:
    result = row.get("result", "")
    if not result:
        return "pending"
    margin = row.get("result_margin", "")
    if margin:
        return f"{result} ({margin})"
    return result


def _table(headers: list[str], rows: list[list[object]]) -> list[str]:
    output = [
        "| " + " | ".join(_escape(header) for header in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(_escape(value) for value in row) + " |")
    return output


def _summary_lines(rows: list[Row]) -> list[str]:
    props = [row for row in rows if row.get("pick_type", "").lower() == "prop"]
    spreads = [row for row in rows if row.get("pick_type", "").lower() == "spread"]
    graded = [row for row in rows if row.get("result")]
    wins = sum(1 for row in graded if row.get("result", "").lower() == "win")
    losses = sum(1 for row in graded if row.get("result", "").lower() == "loss")
    pushes = sum(1 for row in graded if row.get("result", "").lower() == "push")

    lines = [
        f"- Props shown: {len(props)}",
        f"- Spread picks shown: {len(spreads)}",
    ]
    if graded:
        lines.append(f"- Graded record: {wins}-{losses}-{pushes}")
    else:
        lines.append("- Graded record: pending")
    return lines


def write_report(
    date: str,
    picks_path: Path,
    output_dir: Path,
    graded_path: Path | None = None,
    summary_path: Path | None = None,
) -> tuple[Path, list[Row]]:
    graded_rows = read_csv(graded_path) if graded_path and graded_path.exists() else []
    rows = graded_rows or read_csv(picks_path)
    if not rows:
        raise FileNotFoundError(f"No picks found for report: {picks_path}")

    props = [row for row in rows if row.get("pick_type", "").lower() == "prop"]
    spreads = [row for row in rows if row.get("pick_type", "").lower() == "spread"]
    model_summary = read_csv(summary_path) if summary_path and summary_path.exists() else []
    source = graded_path if graded_rows and graded_path else picks_path

    lines: list[str] = [
        f"# NBA Picks Report - {date}",
        "",
        f"Source: `{source}`",
        "",
        "## Quick summary",
        "",
        *_summary_lines(rows),
        "",
        "## Top 5 player props",
        "",
    ]

    lines.extend(
        _table(
            [
                "Rank",
                "Pick",
                "Game",
                "Confidence",
                "Projection",
                "Edge",
                "Odds",
                "Result",
            ],
            [
                [
                    row.get("rank", ""),
                    _pick_text(row),
                    _game_text(row),
                    row.get("confidence_score", ""),
                    row.get("projected_value", ""),
                    row.get("edge", ""),
                    row.get("american_odds", ""),
                    _result_text(row),
                ]
                for row in props
            ],
        )
    )
    lines.extend(["", "## Number 1 spread pick", ""])

    if spreads:
        lines.extend(
            _table(
                [
                    "Rank",
                    "Pick",
                    "Game",
                    "Confidence",
                    "Projected Margin",
                    "Edge",
                    "Odds",
                    "Result",
                ],
                [
                    [
                        row.get("rank", ""),
                        _pick_text(row),
                        _game_text(row),
                        row.get("confidence_score", ""),
                        row.get("projected_value", ""),
                        row.get("edge", ""),
                        row.get("american_odds", ""),
                        _result_text(row),
                    ]
                    for row in spreads
                ],
            )
        )
    else:
        lines.append("No spread pick found.")

    lines.extend(["", "## Why the model liked each pick", ""])
    for row in rows:
        lines.extend(
            [
                f"### {row.get('pick_type', '').title()} #{row.get('rank', '')}: {_pick_text(row)}",
                "",
                f"- Game: {_game_text(row)}",
                f"- Confidence: {row.get('confidence_score', '')}",
                f"- Edge: {row.get('edge', '')}",
                f"- Top factors: {row.get('top_factors', '') or 'none listed'}",
                f"- Risk flags: {row.get('risk_flags', '') or 'none'}",
                f"- Notes: {row.get('notes', '') or 'none'}",
                f"- Result: {_result_text(row)}",
                "",
            ]
        )

    if model_summary:
        lines.extend(["## Learning summary", ""])
        lines.extend(
            _table(
                [
                    "Segment",
                    "Sample",
                    "Record",
                    "Win Rate",
                    "Avg Confidence",
                    "Adjustment",
                ],
                [
                    [
                        f"{row.get('segment_type', '')}:{row.get('segment', '')}",
                        row.get("sample_size", ""),
                        f"{row.get('wins', '')}-{row.get('losses', '')}-{row.get('pushes', '')}",
                        row.get("win_rate", ""),
                        row.get("avg_confidence", ""),
                        row.get("calibration_adjustment", ""),
                    ]
                    for row in model_summary
                ],
            )
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"picks_report_{date}.md"
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return output_path, rows

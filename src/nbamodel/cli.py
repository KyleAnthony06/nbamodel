from __future__ import annotations

import argparse
from pathlib import Path

from nbamodel.config import load_config
from nbamodel.grading import grade_picks
from nbamodel.report import write_report
from nbamodel.scoring import rank_picks


def _default_props_path(date: str) -> Path:
    return Path(f"data/input/props_{date}.csv")


def _default_spreads_path(date: str) -> Path:
    return Path(f"data/input/spreads_{date}.csv")


def _default_picks_path(date: str) -> Path:
    return Path(f"data/output/picks_{date}.csv")


def _default_graded_path(date: str) -> Path:
    return Path(f"data/results/graded_picks_{date}.csv")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nbamodel",
        description="Rank NBA player props and spread picks from daily CSV inputs.",
    )
    parser.add_argument(
        "--config",
        default="config/weights.json",
        type=Path,
        help="Path to the model weight configuration.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="Generate top 5 props and top spread.")
    generate.add_argument("--date", required=True, help="Slate date in YYYY-MM-DD format.")
    generate.add_argument("--props", type=Path, help="Daily prop candidates CSV.")
    generate.add_argument("--spreads", type=Path, help="Daily spread candidates CSV.")
    generate.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/output"),
        help="Directory where picks_DATE.csv is written.",
    )
    generate.add_argument(
        "--report-dir",
        type=Path,
        default=Path("reports"),
        help="Directory where picks_report_DATE.md is written.",
    )

    grade = subparsers.add_parser("grade", help="Grade generated picks with final results.")
    grade.add_argument("--date", required=True, help="Slate date in YYYY-MM-DD format.")
    grade.add_argument("--picks", type=Path, help="Generated picks CSV.")
    grade.add_argument(
        "--prop-actuals",
        type=Path,
        help="Player results CSV. Defaults to data/results/player_actuals_DATE.csv.",
    )
    grade.add_argument(
        "--spread-actuals",
        type=Path,
        help="Game results CSV. Defaults to data/results/spread_actuals_DATE.csv.",
    )
    grade.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/results"),
        help="Directory where graded_picks_DATE.csv is written.",
    )
    grade.add_argument(
        "--report-dir",
        type=Path,
        default=Path("reports"),
        help="Directory where picks_report_DATE.md is written.",
    )

    report = subparsers.add_parser("report", help="Create a readable Markdown picks report.")
    report.add_argument("--date", required=True, help="Slate date in YYYY-MM-DD format.")
    report.add_argument("--picks", type=Path, help="Generated picks CSV.")
    report.add_argument("--graded", type=Path, help="Optional graded picks CSV.")
    report.add_argument("--summary", type=Path, help="Optional model summary CSV.")
    report.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reports"),
        help="Directory where picks_report_DATE.md is written.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = load_config(args.config)

    if args.command == "generate":
        output_path, picks = rank_picks(
            date=args.date,
            props_path=args.props or _default_props_path(args.date),
            spreads_path=args.spreads or _default_spreads_path(args.date),
            output_dir=args.output_dir,
            config=config,
        )
        report_path, _ = write_report(
            date=args.date,
            picks_path=output_path,
            output_dir=args.report_dir,
        )
        print(f"Wrote {len(picks)} picks to {output_path}")
        print(f"Wrote readable report to {report_path}")
        return 0

    if args.command == "grade":
        picks_path = args.picks or _default_picks_path(args.date)
        graded_path, summary_path, graded = grade_picks(
            date=args.date,
            picks_path=picks_path,
            prop_actuals_path=args.prop_actuals or Path(f"data/results/player_actuals_{args.date}.csv"),
            spread_actuals_path=args.spread_actuals or Path(f"data/results/spread_actuals_{args.date}.csv"),
            output_dir=args.output_dir,
            config=config,
        )
        report_path, _ = write_report(
            date=args.date,
            picks_path=picks_path,
            graded_path=graded_path,
            summary_path=summary_path,
            output_dir=args.report_dir,
        )
        print(f"Graded {len(graded)} picks to {graded_path}")
        print(f"Updated learning summary at {summary_path}")
        print(f"Updated readable report at {report_path}")
        return 0

    if args.command == "report":
        learning_config = config.get("learning", {})
        report_path, rows = write_report(
            date=args.date,
            picks_path=args.picks or _default_picks_path(args.date),
            graded_path=args.graded or _default_graded_path(args.date),
            summary_path=args.summary or Path(learning_config.get("summary_path", "data/history/model_summary.csv")),
            output_dir=args.output_dir,
        )
        print(f"Wrote readable report with {len(rows)} picks to {report_path}")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

from pathlib import Path

from nbamodel.config import load_config
from nbamodel.grading import grade_picks
from nbamodel.scoring import rank_picks


def test_rank_picks_writes_five_props_and_one_spread(tmp_path: Path) -> None:
    config = load_config(Path("config/weights.json"))

    output_path, picks = rank_picks(
        date="2026-01-01",
        props_path=Path("data/input/props_2026-01-01.csv"),
        spreads_path=Path("data/input/spreads_2026-01-01.csv"),
        output_dir=tmp_path,
        config=config,
    )

    assert output_path.exists()
    assert len([pick for pick in picks if pick["pick_type"] == "prop"]) == 5
    assert len([pick for pick in picks if pick["pick_type"] == "spread"]) == 1
    assert picks[0]["rank"] == "1"
    assert float(picks[0]["confidence_score"]) >= float(picks[-1]["confidence_score"])


def test_grade_picks_updates_history_and_summary(tmp_path: Path) -> None:
    config = load_config(Path("config/weights.json"))
    config["learning"]["history_path"] = str(tmp_path / "pick_history.csv")
    config["learning"]["summary_path"] = str(tmp_path / "model_summary.csv")
    picks_path, _ = rank_picks(
        date="2026-01-01",
        props_path=Path("data/input/props_2026-01-01.csv"),
        spreads_path=Path("data/input/spreads_2026-01-01.csv"),
        output_dir=tmp_path,
        config=config,
    )

    graded_path, summary_path, graded = grade_picks(
        date="2026-01-01",
        picks_path=picks_path,
        prop_actuals_path=Path("data/results/player_actuals_2026-01-01.csv"),
        spread_actuals_path=Path("data/results/spread_actuals_2026-01-01.csv"),
        output_dir=tmp_path,
        config=config,
    )

    assert graded_path.exists()
    assert summary_path.exists()
    assert len(graded) == 6
    assert {row["result"] for row in graded} <= {"win", "loss", "push"}

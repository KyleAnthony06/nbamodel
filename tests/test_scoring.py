import unittest
from pathlib import Path

from nbamodel.config import load_config
from nbamodel.grading import grade_picks
from nbamodel.scoring import rank_picks


class ScoringWorkflowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_path = Path("data/output/test_tmp")
        self.tmp_path.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        for path in sorted(self.tmp_path.glob("*"), reverse=True):
            path.unlink()
        self.tmp_path.rmdir()

    def test_rank_picks_writes_five_props_and_one_spread(self) -> None:
        config = load_config(Path("config/weights.json"))

        output_path, picks = rank_picks(
            date="2026-01-01",
            props_path=Path("data/input/props_2026-01-01.csv"),
            spreads_path=Path("data/input/spreads_2026-01-01.csv"),
            output_dir=self.tmp_path,
            config=config,
        )

        self.assertTrue(output_path.exists())
        self.assertEqual(len([pick for pick in picks if pick["pick_type"] == "prop"]), 5)
        self.assertEqual(len([pick for pick in picks if pick["pick_type"] == "spread"]), 1)
        self.assertEqual(picks[0]["rank"], "1")
        self.assertGreaterEqual(float(picks[0]["confidence_score"]), float(picks[-1]["confidence_score"]))

    def test_grade_picks_updates_history_and_summary(self) -> None:
        config = load_config(Path("config/weights.json"))
        config["learning"]["history_path"] = str(self.tmp_path / "pick_history.csv")
        config["learning"]["summary_path"] = str(self.tmp_path / "model_summary.csv")
        picks_path, _ = rank_picks(
            date="2026-01-01",
            props_path=Path("data/input/props_2026-01-01.csv"),
            spreads_path=Path("data/input/spreads_2026-01-01.csv"),
            output_dir=self.tmp_path,
            config=config,
        )

        graded_path, summary_path, graded = grade_picks(
            date="2026-01-01",
            picks_path=picks_path,
            prop_actuals_path=Path("data/results/player_actuals_2026-01-01.csv"),
            spread_actuals_path=Path("data/results/spread_actuals_2026-01-01.csv"),
            output_dir=self.tmp_path,
            config=config,
        )

        self.assertTrue(graded_path.exists())
        self.assertTrue(summary_path.exists())
        self.assertEqual(len(graded), 6)
        self.assertLessEqual({row["result"] for row in graded}, {"win", "loss", "push"})


if __name__ == "__main__":
    unittest.main()

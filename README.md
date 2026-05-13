# nbamodel

CSV-driven NBA research model for ranking:

- the 5 player props with the strongest confidence score on a slate
- the 1 spread pick with the strongest confidence score on that slate

The model is designed to be transparent. You provide daily CSV inputs for lines,
projections, injuries, matchup context, shot profile, and team situation. The CLI
scores every candidate, writes the picks to a CSV, then can grade those picks the
next day and update a history file that calibrates future confidence.

> This is a research and tracking tool, not a guarantee of betting outcomes.

## Folders

```text
config/                 Model weights and learning settings
data/input/             Daily prop and spread candidate CSVs
data/output/            Generated picks CSVs
data/results/           Actual player/game result CSVs and graded outputs
data/history/           Long-term pick history and model summary
src/nbamodel/           Python package and CLI
tests/                  Smoke tests
```

## Daily workflow

Install the local package once:

```bash
python -m pip install -e .
```

1. Create or copy the slate files:

   - `data/input/props_YYYY-MM-DD.csv`
   - `data/input/spreads_YYYY-MM-DD.csv`

2. Generate picks:

   ```bash
   python -m nbamodel generate --date YYYY-MM-DD
   ```

   Output:

   - `data/output/picks_YYYY-MM-DD.csv`

3. The next day, fill in actual results:

   - `data/results/player_actuals_YYYY-MM-DD.csv`
   - `data/results/spread_actuals_YYYY-MM-DD.csv`

4. Grade the slate:

   ```bash
   python -m nbamodel grade --date YYYY-MM-DD
   ```

   Outputs:

   - `data/results/graded_picks_YYYY-MM-DD.csv`
   - `data/history/pick_history.csv`
   - `data/history/model_summary.csv`

## Example

The repo includes example files for `2026-01-01`.

```bash
python -m nbamodel generate --date 2026-01-01
python -m nbamodel grade --date 2026-01-01
```

## How scoring works

### Player props

Each candidate prop gets a confidence score from:

- projection edge versus the posted line
- recent form and season-to-recent trend
- shot/attempt trend
- defensive matchup by opponent rank against that market
- opponent defensive rating
- injury-driven usage changes
- projected minutes and minutes floor
- shot quality and volume stability
- team total, pace, rest, and back-to-back spot
- price/odds quality
- injury/news risk
- historical calibration from previously graded picks

The top 5 props are written to the picks CSV.

### Spread

Each spread candidate gets a confidence score from:

- projected margin versus the spread
- team and opponent power ratings
- injury net-rating impact
- rest and schedule spot
- market movement and consensus edge
- pace, rebounding, turnover, clutch, and motivation edges
- price/odds quality
- news risk
- historical calibration from previously graded picks

The top spread candidate is written to the same picks CSV.

## CSV schemas

Use the included example files as templates.

### Prop candidates

`data/input/props_YYYY-MM-DD.csv`

Required columns:

```text
date,game_id,player,team,opponent,market,side,line,american_odds,book,
projected_value,projection_source,projected_minutes,minutes_floor,usage_rate,
season_avg,last_5_avg,last_10_avg,season_attempts,last_5_attempts,team_total,
game_total,pace,opp_def_rating,opp_rank_vs_market,opp_allowed_per_game,
home_away,rest_days,is_back_to_back,teammates_out,injury_usage_bump,
primary_defender,defender_def_rating,shot_quality,shot_volume_stability,
news_risk,notes
```

Notes:

- `side` should be `over` or `under`.
- `opp_rank_vs_market`: use `1` for the toughest defense/fewest allowed and
  `30` for the softest/most allowed.
- `shot_quality`, `shot_volume_stability`, and `news_risk` are decimal scores
  from `0` to `1`.
- `injury_usage_bump` is percentage-point usage change, positive when the
  player's role improves.

### Spread candidates

`data/input/spreads_YYYY-MM-DD.csv`

Required columns:

```text
date,game_id,team,opponent,line,american_odds,book,projected_margin,
team_power_rating,opponent_power_rating,injury_net_rating,schedule_spot,
rest_advantage,travel_spot,market_consensus,opening_line,current_line,
pace_edge,rebounding_edge,turnover_edge,clutch_edge,motivation,news_risk,notes
```

Notes:

- `line` is from the team's perspective. Example: favorite by 3.5 is `-3.5`;
  underdog getting 4.5 is `4.5`.
- `projected_margin` is team score minus opponent score.

### Player actuals

`data/results/player_actuals_YYYY-MM-DD.csv`

```text
date,player,team,market,actual_value
```

### Spread actuals

`data/results/spread_actuals_YYYY-MM-DD.csv`

```text
date,game_id,team,team_score,opponent_score
```

## Learning loop

After grading, the tool appends the results to `data/history/pick_history.csv`
and rebuilds `data/history/model_summary.csv`.

Future runs read the history and apply small confidence adjustments by:

- pick type
- market
- pick type + market
- market + side

The default settings require at least 20 graded samples before a segment changes
future confidence. Edit `config/weights.json` to change the threshold, maximum
adjustment, or feature weights.

## Tests

```bash
python -m pytest
```
# NBA Picks Report - 2026-05-13

Source: `data/output/picks_2026-05-13.csv`

## Quick summary

- Props shown: 5
- Spread picks shown: 1
- Graded record: pending

## Top 5 player props

| Rank | Pick | Game | Confidence | Projection | Edge | Odds | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Donovan Mitchell UNDER 3.5 assists | CLE vs DET (CLE-DET-G5) | 69.70 | 2.7 | 0.80 | -105 | pending |
| 2 | Jarrett Allen UNDER 7.5 rebounds | CLE vs DET (CLE-DET-G5) | 69.32 | 5.4 | 2.10 | 100 | pending |
| 3 | Jalen Duren UNDER 9.5 rebounds | DET vs CLE (CLE-DET-G5) | 68.31 | 7.2 | 2.30 | -115 | pending |
| 4 | Jalen Duren UNDER 12.5 points | DET vs CLE (CLE-DET-G5) | 67.78 | 10.0 | 2.50 | -115 | pending |
| 5 | Ausar Thompson OVER 6.5 rebounds | DET vs CLE (CLE-DET-G5) | 64.84 | 8.0 | 1.50 | -130 | pending |

## Number 1 spread pick

| Rank | Pick | Game | Confidence | Projected Margin | Edge | Odds | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CLE +4.5 | CLE vs DET (CLE-DET-G5) | 55.91 | -2.20 | 2.30 | -115 | pending |

## Why the model liked each pick

### Prop #1: Donovan Mitchell UNDER 3.5 assists

- Game: CLE vs DET (CLE-DET-G5)
- Confidence: 69.70
- Edge: 0.80
- Top factors: projection_edge=+3.20; matchup=+1.40; recent_form=+1.20; defense_rating=+0.70; trend=+0.70
- Risk flags: none
- Notes: BetMGM notes Mitchell has not topped three assists in any Cleveland playoff loss and Detroit allows the fewest assists
- Result: pending

### Prop #2: Jarrett Allen UNDER 7.5 rebounds

- Game: CLE vs DET (CLE-DET-G5)
- Confidence: 69.32
- Edge: 2.10
- Top factors: projection_edge=+3.20; recent_form=+1.20; matchup=+1.11; defense_rating=+0.70; trend=+0.70
- Risk flags: none
- Notes: Averaging 4.8 rebounds in series; stayed under 7.5 in 9 of 11 playoff games
- Result: pending

### Prop #3: Jalen Duren UNDER 9.5 rebounds

- Game: DET vs CLE (CLE-DET-G5)
- Confidence: 68.31
- Edge: 2.30
- Top factors: projection_edge=+3.20; recent_form=+1.20; matchup=+0.82; trend=+0.70; volume_stability=+0.51
- Risk flags: none
- Notes: Action Network notes 32% rebounding rate and only six combined rebounds over last two games
- Result: pending

### Prop #4: Jalen Duren UNDER 12.5 points

- Game: DET vs CLE (CLE-DET-G5)
- Confidence: 67.78
- Edge: 2.50
- Top factors: projection_edge=+3.20; recent_form=+1.10; matchup=+0.72; volume_stability=+0.72; trend=+0.70
- Risk flags: none
- Notes: Under 12.5 points in all four games of this series; Cleveland has focused on suffocating Duren
- Result: pending

### Prop #5: Ausar Thompson OVER 6.5 rebounds

- Game: DET vs CLE (CLE-DET-G5)
- Confidence: 64.84
- Edge: 1.50
- Top factors: projection_edge=+3.20; recent_form=+1.20; trend=+0.70; attempt_trend=+0.69; volume_stability=+0.67
- Risk flags: none
- Notes: BetMGM notes 8.2 rebounds on 13 chances in six home playoff games; Harris out should keep wing rebound minutes strong
- Result: pending

### Spread #1: CLE +4.5

- Game: CLE vs DET (CLE-DET-G5)
- Confidence: 55.91
- Edge: 2.30
- Top factors: projection_edge=+1.12; consensus_edge=+0.60; injury_net_rating=+0.44; motivation=+0.23; power_rating=-0.21
- Risk flags: none
- Notes: Rebuilt after user-reported Tobias Harris out; best cushion if +4.5 is still available
- Result: pending

## Learning summary

| Segment | Sample | Record | Win Rate | Avg Confidence | Adjustment |
| --- | --- | --- | --- | --- | --- |
| market:assists | 1 | 1-0-0 | 1.000 | 66.48 | 0.00 |
| market:points | 2 | 2-0-0 | 1.000 | 67.83 | 0.00 |
| market:rebounds | 1 | 0-1-0 | 0.000 | 66.52 | 0.00 |
| market:spread | 1 | 1-0-0 | 1.000 | 59.48 | 0.00 |
| market:threes | 1 | 1-0-0 | 1.000 | 67.53 | 0.00 |
| market_side:assists:under | 1 | 1-0-0 | 1.000 | 66.48 | 0.00 |
| market_side:points:over | 1 | 1-0-0 | 1.000 | 71.31 | 0.00 |
| market_side:points:under | 1 | 1-0-0 | 1.000 | 64.35 | 0.00 |
| market_side:rebounds:over | 1 | 0-1-0 | 0.000 | 66.52 | 0.00 |
| market_side:spread:team | 1 | 1-0-0 | 1.000 | 59.48 | 0.00 |
| market_side:threes:over | 1 | 1-0-0 | 1.000 | 67.53 | 0.00 |
| type:prop | 5 | 4-1-0 | 0.800 | 67.24 | 0.00 |
| type:spread | 1 | 1-0-0 | 1.000 | 59.48 | 0.00 |

# NBA Picks Report - 2026-01-01

Source: `data/results/graded_picks_2026-01-01.csv`

## Quick summary

- Props shown: 5
- Spread picks shown: 1
- Graded record: 5-1-0

## Top 5 player props

| Rank | Pick | Game | Confidence | Projection | Edge | Odds | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Example Guard OVER 24.5 points | AAA vs BBB (EX1) | 71.31 | 29.1 | 4.60 | -112 | win (6.50) |
| 2 | Example Shooter OVER 2.5 threes | DDD vs CCC (EX2) | 67.53 | 3.4 | 0.90 | 110 | win (0.50) |
| 3 | Example Center OVER 10.5 rebounds | BBB vs AAA (EX1) | 66.52 | 12.3 | 1.80 | -105 | loss (-1.50) |
| 4 | Example Wing UNDER 5.5 assists | CCC vs DDD (EX2) | 66.48 | 4.1 | 1.40 | -118 | win (1.50) |
| 5 | Example Forward UNDER 19.5 points | FFF vs EEE (EX3) | 64.35 | 16.9 | 2.60 | -108 | win (1.50) |

## Number 1 spread pick

| Rank | Pick | Game | Confidence | Projected Margin | Edge | Odds | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | AAA -3.5 | AAA vs BBB (EX1) | 59.48 | 6.40 | 2.90 | -110 | win (3.50) |

## Why the model liked each pick

### Prop #1: Example Guard OVER 24.5 points

- Game: AAA vs BBB (EX1)
- Confidence: 71.31
- Edge: 4.60
- Top factors: projection_edge=+3.20; matchup=+1.01; volume_stability=+0.80; recent_form=+0.76; injury_usage=+0.62
- Risk flags: none
- Notes: High usage with teammate out
- Result: win (6.50)

### Prop #2: Example Shooter OVER 2.5 threes

- Game: DDD vs CCC (EX2)
- Confidence: 67.53
- Edge: 0.90
- Top factors: projection_edge=+3.20; recent_form=+1.20; trend=+0.70; matchup=+0.63; minutes_security=+0.50
- Risk flags: none
- Notes: Good shot diet but news risk
- Result: win (0.50)

### Prop #3: Example Center OVER 10.5 rebounds

- Game: BBB vs AAA (EX1)
- Confidence: 66.52
- Edge: 1.80
- Top factors: projection_edge=+3.05; recent_form=+0.97; matchup=+0.72; volume_stability=+0.62; trend=+0.52
- Risk flags: none
- Notes: Opponent weak on defensive glass
- Result: loss (-1.50)

### Prop #4: Example Wing UNDER 5.5 assists

- Game: CCC vs DDD (EX2)
- Confidence: 66.48
- Edge: 1.40
- Top factors: projection_edge=+3.20; recent_form=+1.20; matchup=+1.01; trend=+0.57; minutes_security=+0.50
- Risk flags: none
- Notes: Lower on-ball role
- Result: win (1.50)

### Prop #5: Example Forward UNDER 19.5 points

- Game: FFF vs EEE (EX3)
- Confidence: 64.35
- Edge: 2.60
- Top factors: projection_edge=+2.37; matchup=+1.11; recent_form=+0.74; volume_stability=+0.72; defense_rating=+0.53
- Risk flags: none
- Notes: Tough individual matchup
- Result: win (1.50)

### Spread #1: AAA -3.5

- Game: AAA vs BBB (EX1)
- Confidence: 59.48
- Edge: 2.90
- Top factors: projection_edge=+1.41; power_rating=+0.67; consensus_edge=-0.60; rest_advantage=+0.40; injury_net_rating=+0.32
- Risk flags: none
- Notes: Home team has healthier rotation
- Result: win (3.50)

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

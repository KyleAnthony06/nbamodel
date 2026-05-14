# NBA Picks Report - 2026-05-13

Source: `data/results/graded_picks_2026-05-13.csv`

## Quick summary

- Props shown: 5
- Spread picks shown: 1
- Graded record: 3-3-0

## Top 5 player props

| Rank | Pick | Game | Confidence | Projection | Edge | Odds | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Donovan Mitchell UNDER 3.5 assists | CLE vs DET (CLE-DET-G5) | 70.06 | 2.7 | 0.80 | -105 | win (0.50) |
| 2 | Jarrett Allen UNDER 7.5 rebounds | CLE vs DET (CLE-DET-G5) | 69.32 | 5.4 | 2.10 | 100 | loss (-2.50) |
| 3 | Jalen Duren UNDER 9.5 rebounds | DET vs CLE (CLE-DET-G5) | 67.99 | 7.4 | 2.10 | -115 | win (4.50) |
| 4 | Jalen Duren UNDER 12.5 points | DET vs CLE (CLE-DET-G5) | 67.43 | 10.0 | 2.50 | -115 | win (3.50) |
| 5 | Tobias Harris OVER 18.5 points | DET vs CLE (CLE-DET-G5) | 62.74 | 21.2 | 2.70 | -108 | loss (-5.50) |

## Number 1 spread pick

| Rank | Pick | Game | Confidence | Projected Margin | Edge | Odds | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DET -3.5 | DET vs CLE (CLE-DET-G5) | 56.65 | 6.80 | 3.30 | -112 | loss (-7.50) |

## Why the model liked each pick

### Prop #1: Donovan Mitchell UNDER 3.5 assists

- Game: CLE vs DET (CLE-DET-G5)
- Confidence: 70.06
- Edge: 0.80
- Top factors: projection_edge=+3.20; matchup=+1.40; recent_form=+1.20; defense_rating=+0.70; trend=+0.70
- Risk flags: none
- Notes: BetMGM notes Mitchell has not topped three assists in any Cleveland playoff loss and Detroit allows the fewest assists
- Result: win (0.50)

### Prop #2: Jarrett Allen UNDER 7.5 rebounds

- Game: CLE vs DET (CLE-DET-G5)
- Confidence: 69.32
- Edge: 2.10
- Top factors: projection_edge=+3.20; recent_form=+1.20; matchup=+1.11; defense_rating=+0.70; trend=+0.70
- Risk flags: none
- Notes: Averaging 4.8 rebounds in series; stayed under 7.5 in 9 of 11 playoff games
- Result: loss (-2.50)

### Prop #3: Jalen Duren UNDER 9.5 rebounds

- Game: DET vs CLE (CLE-DET-G5)
- Confidence: 67.99
- Edge: 2.10
- Top factors: projection_edge=+3.20; recent_form=+1.20; matchup=+0.82; trend=+0.70; volume_stability=+0.51
- Risk flags: none
- Notes: Action Network notes 32% rebounding rate and only six combined rebounds over last two games
- Result: win (4.50)

### Prop #4: Jalen Duren UNDER 12.5 points

- Game: DET vs CLE (CLE-DET-G5)
- Confidence: 67.43
- Edge: 2.50
- Top factors: projection_edge=+3.20; recent_form=+1.10; matchup=+0.72; volume_stability=+0.72; trend=+0.70
- Risk flags: none
- Notes: Under 12.5 points in all four games of this series; Cleveland has focused on suffocating Duren
- Result: win (3.50)

### Prop #5: Tobias Harris OVER 18.5 points

- Game: DET vs CLE (CLE-DET-G5)
- Confidence: 62.74
- Edge: 2.70
- Top factors: projection_edge=+2.59; recent_form=+0.81; volume_stability=+0.77; matchup=+0.53; trend=+0.44
- Risk flags: none
- Notes: Harris confirmed active; over this number in eight of last nine before Game 4 miss
- Result: loss (-5.50)

### Spread #1: DET -3.5

- Game: DET vs CLE (CLE-DET-G5)
- Confidence: 56.65
- Edge: 3.30
- Top factors: projection_edge=+1.60; consensus_edge=-0.60; schedule_spot=+0.48; power_rating=+0.41; motivation=+0.38
- Risk flags: none
- Notes: Harris confirmed active; FanDuel listed Pistons -3.5, home team has won every game, and Cleveland is winless on road this postseason
- Result: loss (-7.50)

## Learning summary

| Segment | Sample | Record | Win Rate | Avg Confidence | Adjustment |
| --- | --- | --- | --- | --- | --- |
| market:assists | 2 | 2-0-0 | 1.000 | 68.27 | 0.00 |
| market:points | 4 | 3-1-0 | 0.750 | 66.46 | 0.00 |
| market:rebounds | 3 | 1-2-0 | 0.333 | 67.94 | 0.00 |
| market:spread | 2 | 1-1-0 | 0.500 | 58.06 | 0.00 |
| market:threes | 1 | 1-0-0 | 1.000 | 67.53 | 0.00 |
| market_side:assists:under | 2 | 2-0-0 | 1.000 | 68.27 | 0.00 |
| market_side:points:over | 2 | 1-1-0 | 0.500 | 67.03 | 0.00 |
| market_side:points:under | 2 | 2-0-0 | 1.000 | 65.89 | 0.00 |
| market_side:rebounds:over | 1 | 0-1-0 | 0.000 | 66.52 | 0.00 |
| market_side:rebounds:under | 2 | 1-1-0 | 0.500 | 68.66 | 0.00 |
| market_side:spread:team | 2 | 1-1-0 | 0.500 | 58.06 | 0.00 |
| market_side:threes:over | 1 | 1-0-0 | 1.000 | 67.53 | 0.00 |
| type:prop | 10 | 7-3-0 | 0.700 | 67.37 | 0.00 |
| type:spread | 2 | 1-1-0 | 0.500 | 58.06 | 0.00 |

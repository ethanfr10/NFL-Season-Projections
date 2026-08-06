## NFL Season Projection Model

An end-to-end NFL forecasting system that projects team strength, game outcomes, season records, and playoff probabilities using team performance, roster movement, coaching changes, schedule context, and Monte Carlo simulation.

## Projecting the 2026 NFL Season Through Team Strength, Roster Construction, Coaching, and Schedule Simulation

NFL teams can change dramatically from one season to the next.

A team may improve its quarterback situation, replace several starters, hire a new coaching staff, suffer important injuries, face a more difficult schedule, or simply regress after winning an unsustainable number of close games.

Because of this, projecting an NFL season requires more than looking at the previous year’s record.

This project is an end-to-end NFL forecasting system designed to estimate how strong every team will be entering the 2026 season, how likely each team is to win every game, and what range of season outcomes is most realistic.

The final model will produce:

* Expected wins
* Most likely record
* Full record distributions
* Game-by-game win probabilities
* Division championship probabilities
* Wild-card and playoff probabilities
* Conference and Super Bowl probabilities
* Offensive, defensive, and special-teams ratings
* Position-group strength ratings
* Schedule difficulty
* Roster improvement and decline
* Coaching and continuity adjustments
* Explanations for each team’s projection

The objective is not only to predict what will happen, but to explain **why the model believes it will happen**.

---

## The Main Question

> How many games should each NFL team be expected to win in 2026 after accounting for its underlying performance, roster changes, coaching structure, player development, injuries, continuity, and schedule?

Instead of assigning every team one definite record, the model will estimate a range of possible outcomes.

For example:

| Metric               | Example Projection |
| -------------------- | -----------------: |
| Expected Wins        |               10.4 |
| Most Likely Record   |               10–7 |
| 90% Win Range        |               7–13 |
| Playoff Probability  |                68% |
| Division Probability |                34% |

A team projected for 10.4 wins is not guaranteed to finish 10–7. Injuries, turnovers, close games, weather, player development, and random variation can all affect the final result.

The simulation component is designed to represent that uncertainty.

---

## Project Philosophy

This project is built around four principles.

### 1. Records do not tell the entire story

A team’s win-loss record can be heavily affected by:

* One-score games
* Turnover luck
* Defensive touchdowns
* Opponent injuries
* Strength of schedule
* Field-goal variance
* Overtime outcomes

The model will therefore rely heavily on underlying performance measures such as efficiency, success rate, expected wins, and point differential.

### 2. Every projection should be explainable

The project will not simply state that a team improved.

It will measure the possible causes of improvement, including:

* Better quarterback play
* Stronger offensive-line continuity
* Returning injured starters
* Free-agent additions
* Player departures
* Drafted players
* Coaching changes
* Coordinator continuity
* Schedule difficulty

Each team projection will include an explanation of the factors pushing its expected record upward or downward.

### 3. Coaching should be measured rather than guessed

Coaching changes are often discussed subjectively.

This project will create a separate coaching dataset that tracks:

* Head coach changes
* Offensive coordinator changes
* Defensive coordinator changes
* Play-calling experience
* Previous offensive or defensive performance
* Scheme continuity
* Quarterback and coordinator continuity
* Returning starters
* Fourth-down aggressiveness
* Pass rate over expectation
* Prior head-coaching experience

Historical results will be used to estimate how coaching changes typically affect future team performance.

### 4. Uncertainty should be shown honestly

NFL seasons are difficult to predict.

The model will report:

* Probability distributions
* Confidence intervals
* Simulation ranges
* Calibration results
* Model errors
* Alternative scenarios

The purpose is not to pretend that the future is certain. The purpose is to estimate which outcomes are most likely.

---

## Project Structure

The system will be developed through several connected components.

### Historical Team Performance

The historical team model will measure offensive, defensive, and special-teams performance using variables such as:

#### Offense

* EPA per play
* Passing EPA
* Rushing EPA
* Success rate
* Explosive-play rate
* Sack rate allowed
* Pressure rate allowed
* Points per drive
* Third-down conversion rate
* Red-zone touchdown rate
* Turnover rate

#### Defense

* EPA allowed per play
* Passing EPA allowed
* Rushing EPA allowed
* Defensive success rate
* Pressure rate
* Sack rate
* Explosive plays allowed
* Points allowed per drive
* Third-down defense
* Red-zone defense
* Takeaway rate

#### Special Teams

* Field-goal performance
* Punt and kick-return value
* Opponent return value
* Starting field position
* Hidden field-position value

#### Team Context

* Point differential
* Expected wins
* One-score record
* Turnover margin
* Strength of schedule
* Home and road performance
* Rest and travel
* Opponent quality

---

## Roster Evaluation

Every team’s offseason will be evaluated through a roster-change model.

The model will track:

* Free-agent additions
* Free-agent departures
* Trades
* Retirements
* Returning injured players
* Draft picks
* Expected starters
* Projected playing time
* Age
* Recent performance
* Position value
* Depth
* Injury history

A simplified player-impact formula will be developed:

```text
Player Impact =
Projected Playing Time
× Performance Rating
× Position Importance
× Availability Adjustment
```

Team roster change will then be estimated as:

```text
Net Roster Change =
Value Added
− Value Lost
+ Expected Development
+ Returning Injury Value
```

---

## Position-Group Ratings

Each team will receive projected ratings for:

* Quarterback
* Running back
* Wide receiver
* Tight end
* Offensive line
* Interior defensive line
* Edge rusher
* Linebacker
* Cornerback
* Safety
* Special teams

Each rating may include:

* Starting talent
* Depth
* Age
* Recent performance
* Projected improvement
* Injury risk
* Continuity
* Expected playing time

---

## Quarterback Projections

Quarterback performance has a major effect on team outcomes, so quarterbacks will receive a dedicated projection model.

Potential variables include:

* EPA per dropback
* Completion percentage over expected
* Sack rate
* Interception rate
* Pressure performance
* Air yards
* Scrambling value
* Designed rushing value
* Age
* Career experience
* Recent multi-year performance
* Offensive coordinator continuity
* Offensive-line strength
* Receiving support
* Injury history

Recent seasons will receive more weight, while extreme performances will be regressed toward the league average.

---

## Coaching and Organizational Structure

The coaching dataset will examine more than whether a team hired a new head coach.

It will include:

* Returning or new head coach
* Returning or new offensive coordinator
* Returning or new defensive coordinator
* New play caller
* Years of play-calling experience
* Previous unit efficiency
* Previous team performance
* Scheme changes
* Quarterback continuity
* Offensive-line continuity
* Returning starters
* First-time head coach
* Previous head-coaching experience
* Staff familiarity
* Years working together

The project will also consider organizational changes that may influence performance, including:

* General manager changes
* Front-office restructuring
* Major scheme transitions
* Quarterback competitions
* Rebuilding timelines
* Changes in roster age
* Changes in team depth
* Changes in expected starter quality

---

## Schedule Model

Every 2026 regular-season game will receive a projected win probability.

Potential game-level variables include:

* Home-team strength
* Away-team strength
* Quarterback difference
* Offensive and defensive matchup
* Home-field advantage
* Rest differential
* Short weeks
* Bye weeks
* Consecutive road games
* Travel distance
* International games
* Divisional matchups
* Weather where appropriate
* Expected injuries and availability

Example output:

| Game              | Win Probability | Expected Margin |
| ----------------- | --------------: | --------------: |
| Team A vs. Team B |             62% |   Team A by 3.4 |

The model will also provide the most important reasons behind each projection.

---

## Season Simulation

After game probabilities are created, the complete NFL season will be simulated at least 25,000 times.

Each simulation will:

1. Simulate every regular-season game.
2. Calculate each team’s final record.
3. Apply playoff qualification and tiebreaking logic.
4. Determine division winners and wild-card teams.
5. Simulate the postseason.
6. Store the results.

The simulations will produce:

* Average wins
* Median wins
* Most likely record
* Probability of each possible record
* Probability of winning at least 10 games
* Probability of finishing below .500
* Division probability
* Playoff probability
* Conference championship probability
* Super Bowl probability
* Top-draft-pick probability

---

## Model Evaluation

The project will use time-based testing rather than randomly mixing games from different seasons.

Example backtests:

* Train through 2021 and predict 2022
* Train through 2022 and predict 2023
* Train through 2023 and predict 2024
* Train through 2024 and predict 2025

Potential evaluation metrics include:

* Mean absolute error for projected wins
* Root mean squared error
* Log loss
* Brier score
* ROC-AUC
* Calibration
* Predicted spread error
* Correct winner percentage

The model will be compared with simple baselines such as:

* Previous-season record
* Previous-season point differential
* Elo ratings
* Home-team win rate
* Market win totals where available

---

## Model Explainability

Predictions should be understandable to technical and non-technical audiences.

The explainability section will include:

* Global feature importance
* Team-specific feature impact
* SHAP values or a similar method
* Confidence intervals
* Scenario analysis
* Sensitivity testing

Example scenario:

> The team is projected for 10.2 wins with its starting quarterback available for the full season. If the quarterback misses six games, the projection decreases to 8.4 wins.

This allows the project to explain both the central projection and the risks surrounding it.

---

## Dashboard

The final Streamlit dashboard will allow users to select any NFL team and view:

* Projected record
* Expected wins
* Playoff probability
* Division probability
* Record distribution
* Offensive ranking
* Defensive ranking
* Position-group ratings
* Schedule difficulty
* Game-by-game win probabilities
* Major additions
* Major departures
* Coaching changes
* Projection strengths
* Projection risks

The dashboard will be designed for fans, analysts, coaches, scouts, executives, and broadcasters.

---

## Planned Development

### Version 0.1 — Project Foundation

* Establish repository structure
* Document project goals
* Collect historical schedules and results
* Collect play-by-play data
* Build initial team-season dataset

### Version 0.2 — Historical Team Ratings

* Calculate team efficiency metrics
* Add expected wins and point differential
* Measure one-score and turnover regression
* Create baseline team-strength ratings

### Version 0.3 — Coaching and Continuity

* Build coaching database
* Track head coach and coordinator changes
* Measure scheme and personnel continuity
* Evaluate historical coaching-change effects

### Version 0.4 — Roster Movement

* Create player and roster tables
* Track additions and departures
* Estimate projected snaps
* Build net roster-change scores

### Version 0.5 — Player Projections

* Build quarterback projections
* Create position-group ratings
* Add age and injury adjustments
* Add rookie impact estimates

### Version 0.6 — Team Projection Model

* Train baseline models
* Compare regression and machine-learning methods
* Produce preseason team-strength projections
* Evaluate historical accuracy

### Version 0.7 — Game Predictions

* Add the 2026 schedule
* Generate game-level win probabilities
* Calculate expected margins
* Add matchup and schedule adjustments

### Version 0.8 — Season Simulation

* Simulate at least 25,000 seasons
* Produce record distributions
* Calculate division and playoff probabilities
* Add postseason simulation

### Version 0.9 — Dashboard and Presentation

* Build the Streamlit dashboard
* Add team pages
* Create recruiter-friendly visualizations
* Add technical and non-technical explanations

### Version 1.0 — Public Release

* Publish final 2026 projections
* Complete documentation
* Release dashboard
* Publish project findings and methodology

---

## Current Status

**Version 0.1 is in progress.**

The current focus is collecting and validating the historical data required to build the first team-strength model.

---

## Project Goal

This project is being built as though it were an internal analytics system for an NFL front office.

Every feature should help answer at least one practical football question:

* How good is this team?
* Why should it improve or decline?
* Which roster changes matter most?
* How much does coaching continuity matter?
* Which position groups create the largest advantage?
* How difficult is the schedule?
* What range of outcomes is realistic?
* What could cause the projection to be wrong?

The final result will be both a predictive model and an accessible explanation of how NFL team strength changes from one season to the next.

# 2026 NFL Season Projection Model

I'm building an NFL projection model to estimate team strength, predict individual games, and simulate the entire 2026 NFL season.

The main idea behind the project is that a team's record from the previous season only tells part of the story. Teams change every offseason through the draft, free agency, trades, injuries, coaching changes, player development, and roster turnover. I want the model to account for those changes while also measuring how good each team actually was before them.

The goal is to build the project from the ground up, starting with raw NFL data and ending with full 2026 season projections.

## Project Goals

The model is designed to answer a few main questions:

- How strong is each NFL team entering 2026?
- Which teams improved or declined during the offseason?
- What is each team's probability of winning an individual game?
- How many games should each team be expected to win?
- What are each team's chances of winning its division, making the playoffs, and winning the Super Bowl?

Rather than predicting one exact record for each team, the final model will simulate the season many times to show the range of possible outcomes.

## Data

The project uses historical NFL data covering several parts of team and player performance, including:

- Game results and schedules
- Player statistics
- Rosters and depth charts
- Snap counts and player participation
- Injuries
- Draft picks
- Contracts and salary cap information
- Trades

These datasets are cleaned and combined to create features that measure team performance, player value, roster strength, continuity, and other factors that could help predict future performance.

## Modeling Process

The project follows the full process from collecting raw data to producing final season projections:

```text
00_Model_Design.ipynb
        ↓
01_Data_Collection.ipynb
        ↓
02_Data_Cleaning.ipynb
        ↓
03_Feature_Engineering.ipynb
        ↓
04_Player_Projections.ipynb
        ↓
05_Team_Strength_Model.ipynb
        ↓
06_Game_Predictions.ipynb
        ↓
07_Monte_Carlo_Simulation.ipynb
        ↓
08_Model_Evaluation.ipynb
        ↓
09_Dashboard.ipynb
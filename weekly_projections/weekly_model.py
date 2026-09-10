from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------
# Market line helpers
# ---------------------------------------------------------

def convert_market_spreads(df):

    df = df.copy()

    # nflverse convention:
    # positive spread_line = home favorite
    # negative spread_line = away favorite

    df["home_spread"] = -df["spread_line"]
    df["away_spread"] = df["spread_line"]

    df["market_favorite"] = np.where(
        df["home_spread"] < 0,
        df["home_team"],
        np.where(
            df["away_spread"] < 0,
            df["away_team"],
            "PICK"
        )
    )

    return df


# ---------------------------------------------------------
# ATS helpers
# ---------------------------------------------------------

def add_ats_projections(df):

    df = df.copy()

    # Convert model margin into sportsbook-style spreads
    df["model_home_spread"] = -df["expected_home_margin"]
    df["model_away_spread"] = df["expected_home_margin"]

    # Difference between model and sportsbook
    df["home_ats_edge"] = (
        df["home_spread"]
        - df["model_home_spread"]
    )

    df["away_ats_edge"] = (
        df["away_spread"]
        - df["model_away_spread"]
    )

    df["ats_pick"] = np.where(
        df["home_ats_edge"] > 0,
        df["home_team"],
        np.where(
            df["away_ats_edge"] > 0,
            df["away_team"],
            "PUSH"
        )
    )

    df["ats_difference"] = (
        df[
            [
                "home_ats_edge",
                "away_ats_edge"
            ]
        ]
        .max(axis=1)
    )

    return df


def format_ats_pick(row):

    if row["ats_pick"] == "PUSH":
        return "PUSH"

    if row["ats_pick"] == row["home_team"]:
        line = row["home_spread"]
    else:
        line = row["away_spread"]

    if line > 0:
        return f"{row['ats_pick']} +{line:.1f}"

    return f"{row['ats_pick']} {line:.1f}"


def format_market_spread(row):

    if row["home_spread"] < 0:
        return (
            f"{row['home_team']} "
            f"{row['home_spread']:.1f}"
        )

    if row["away_spread"] < 0:
        return (
            f"{row['away_team']} "
            f"{row['away_spread']:.1f}"
        )

    return "PICK"


def format_model_spread(row):

    if row["model_home_spread"] < 0:
        return (
            f"{row['home_team']} "
            f"{row['model_home_spread']:.1f}"
        )

    if row["model_away_spread"] < 0:
        return (
            f"{row['away_team']} "
            f"{row['model_away_spread']:.1f}"
        )

    return "PICK"


# ---------------------------------------------------------
# Total helpers
# ---------------------------------------------------------

def add_total_projections(
    df,
    projected_total
):

    df = df.copy()

    df["projected_total"] = projected_total

    df["projected_home_score"] = (
        df["projected_total"]
        + df["expected_home_margin"]
    ) / 2

    df["projected_away_score"] = (
        df["projected_total"]
        - df["expected_home_margin"]
    ) / 2

    df["total_difference_signed"] = (
        df["projected_total"]
        - df["total_line"]
    )

    df["total_difference"] = (
        df["total_difference_signed"]
        .abs()
    )

    df["total_pick"] = np.where(
        df["total_difference_signed"] > 0,
        "OVER",
        np.where(
            df["total_difference_signed"] < 0,
            "UNDER",
            "PUSH"
        )
    )

    return df


# ---------------------------------------------------------
# Display helpers
# ---------------------------------------------------------

def add_display_columns(df):

    df = df.copy()

    df["projected_score"] = (
        df["away_team"]
        + " "
        + df["projected_away_score"].round(1).astype(str)
        + " - "
        + df["home_team"]
        + " "
        + df["projected_home_score"].round(1).astype(str)
    )

    df["ats_pick_display"] = (
        df.apply(
            format_ats_pick,
            axis=1
        )
    )

    df["market_spread_display"] = (
        df.apply(
            format_market_spread,
            axis=1
        )
    )

    df["model_spread_display"] = (
        df.apply(
            format_model_spread,
            axis=1
        )
    )

    return df


def build_projection_board(df):

    board = pd.DataFrame(
        {
            "Matchup": (
                df["away_team"]
                + " @ "
                + df["home_team"]
            ),
            "Projected Score": df["projected_score"],
            "SU Pick": df["predicted_winner"],
            "Win Prob": df["predicted_win_probability"],
            "Model Spread": df["model_spread_display"],
            "Market Spread": df["market_spread_display"],
            "ATS Pick": df["ats_pick_display"],
            "ATS Diff": df["ats_difference"],
            "Model Total": df["projected_total"],
            "Market Total": df["total_line"],
            "O/U Pick": df["total_pick"],
            "Total Diff": df["total_difference"]
        }
    )

    return board


def get_biggest_differences(
    projection_board,
    n=5
):

    ats = (
        projection_board[
            [
                "Matchup",
                "Projected Score",
                "Model Spread",
                "Market Spread",
                "ATS Pick",
                "ATS Diff"
            ]
        ]
        .sort_values(
            "ATS Diff",
            ascending=False
        )
        .head(n)
        .copy()
    )

    totals = (
        projection_board[
            [
                "Matchup",
                "Projected Score",
                "Model Total",
                "Market Total",
                "O/U Pick",
                "Total Diff"
            ]
        ]
        .sort_values(
            "Total Diff",
            ascending=False
        )
        .head(n)
        .copy()
    )

    return ats, totals


# ---------------------------------------------------------
# In-season data helpers
# ---------------------------------------------------------

def get_completed_games(
    schedule,
    season,
    target_week
):

    completed = schedule[
        (schedule["season"] == season)
        & (schedule["week"] < target_week)
        & (schedule["home_score"].notna())
        & (schedule["away_score"].notna())
    ].copy()

    return completed


def build_inseason_team_summary(
    completed_games
):

    home = pd.DataFrame(
        {
            "team": completed_games["home_team"],
            "points_for": completed_games["home_score"],
            "points_against": completed_games["away_score"]
        }
    )

    away = pd.DataFrame(
        {
            "team": completed_games["away_team"],
            "points_for": completed_games["away_score"],
            "points_against": completed_games["home_score"]
        }
    )

    team_games = pd.concat(
        [
            home,
            away
        ],
        ignore_index=True
    )

    summary = (
        team_games
        .groupby("team")
        .agg(
            games_played=("team", "size"),
            points_for=("points_for", "sum"),
            points_against=("points_against", "sum")
        )
        .reset_index()
    )

    summary["points_for_per_game"] = (
        summary["points_for"]
        / summary["games_played"]
    )

    summary["points_against_per_game"] = (
        summary["points_against"]
        / summary["games_played"]
    )

    summary["point_diff_per_game"] = (
        summary["points_for_per_game"]
        - summary["points_against_per_game"]
    )

    return summary


# ---------------------------------------------------------
# Saving helpers
# ---------------------------------------------------------

def save_weekly_outputs(
    week_number,
    projection_board,
    ats_differences,
    total_differences,
    output_dir
):

    week_dir = (
        Path(output_dir)
        / f"week_{week_number:02d}"
    )

    week_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    projection_save = projection_board.copy()
    ats_save = ats_differences.copy()
    totals_save = total_differences.copy()

    projection_save["Win Prob"] = (
        projection_save["Win Prob"].round(3)
    )

    projection_save["ATS Diff"] = (
        projection_save["ATS Diff"].round(2)
    )

    projection_save["Model Total"] = (
        projection_save["Model Total"].round(1)
    )

    projection_save["Market Total"] = (
        projection_save["Market Total"].round(1)
    )

    projection_save["Total Diff"] = (
        projection_save["Total Diff"].round(1)
    )

    ats_save["ATS Diff"] = (
        ats_save["ATS Diff"].round(2)
    )

    totals_save["Model Total"] = (
        totals_save["Model Total"].round(1)
    )

    totals_save["Market Total"] = (
        totals_save["Market Total"].round(1)
    )

    totals_save["Total Diff"] = (
        totals_save["Total Diff"].round(1)
    )

    projection_save.to_csv(
        week_dir
        / f"week_{week_number:02d}_projection_board.csv",
        index=False
    )

    ats_save.to_csv(
        week_dir
        / f"week_{week_number:02d}_biggest_ats_differences.csv",
        index=False
    )

    totals_save.to_csv(
        week_dir
        / f"week_{week_number:02d}_biggest_total_differences.csv",
        index=False
    )

    return week_dir
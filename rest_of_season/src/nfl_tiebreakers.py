"""
NFL Tiebreaker Functions
2026 Rest-of-Season Projection Model

Implements the first six NFL division tiebreaking criteria.

Two-team division tiebreakers:
1. Head-to-head record
2. Division record
3. Common games
4. Conference record
5. Strength of victory
6. Strength of schedule

Three-or-more-team division tiebreakers:
1. Head-to-head winning percentage among tied teams
2. Division record
3. Common games
4. Conference record
5. Strength of victory
6. Strength of schedule

If a multi-team tie is reduced to fewer teams, the
appropriate tiebreaking procedure restarts at Step 1.

Later NFL criteria involving points, touchdowns, and
coin tosses are not implemented.

Functions return None when a tie cannot be resolved
using the available information.
"""


def winning_percentage(wins, losses, ties=0):
    """
    Calculate NFL winning percentage.

    A tie counts as half a win and half a loss.
    """

    games = wins + losses + ties

    if games == 0:
        return 0.0

    return (wins + 0.5 * ties) / games


def head_to_head_record(team, opponents, game_results):
    """
    Calculate a team's record against specified opponents.

    game_results contains dictionaries with:
        home_team
        away_team
        winner

    A winner of None represents a tied game.
    """

    wins = 0
    losses = 0
    ties = 0

    for game in game_results:
        home = game["home_team"]
        away = game["away_team"]

        if team == home and away in opponents:
            opponent = away

        elif team == away and home in opponents:
            opponent = home

        else:
            continue

        winner = game["winner"]

        if winner is None:
            ties += 1

        elif winner == team:
            wins += 1

        elif winner == opponent:
            losses += 1

        else:
            raise ValueError(f"Invalid winner: {winner}")

    return {
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "pct": winning_percentage(wins, losses, ties)
    }


def build_season_results(
    completed_games,
    future_games,
    home_wins,
    sim_idx
):
    """
    Combine completed NFL games with the outcomes
    from one Monte Carlo simulation.
    """

    results = []

    # Actual completed games
    for game in completed_games.itertuples(index=False):

        if game.home_score > game.away_score:
            winner = game.home_team

        elif game.away_score > game.home_score:
            winner = game.away_team

        else:
            winner = None

        results.append({
            "home_team": game.home_team,
            "away_team": game.away_team,
            "winner": winner
        })

    # Simulated remaining games
    for game_idx, game in enumerate(
        future_games.itertuples(index=False)
    ):

        home_won = bool(home_wins[sim_idx, game_idx])

        winner = (
            game.home_team
            if home_won
            else game.away_team
        )

        results.append({
            "home_team": game.home_team,
            "away_team": game.away_team,
            "winner": winner
        })

    return results


def common_opponents(team_a, team_b, game_results):
    """
    Find opponents that both teams played.

    Excludes games against each other.
    """

    opponents_a = set()
    opponents_b = set()

    for game in game_results:
        home = game["home_team"]
        away = game["away_team"]

        if home == team_a and away != team_b:
            opponents_a.add(away)

        elif away == team_a and home != team_b:
            opponents_a.add(home)

        if home == team_b and away != team_a:
            opponents_b.add(away)

        elif away == team_b and home != team_a:
            opponents_b.add(home)

    return opponents_a & opponents_b


def common_games_record(
    team,
    shared_opponents,
    game_results
):
    """
    Calculate a team's record against common opponents.
    """

    return head_to_head_record(
        team,
        shared_opponents,
        game_results
    )


def calculate_final_records(game_results):
    """
    Reconstruct final W-L-T records for every team.
    """

    records = {}

    for game in game_results:
        home = game["home_team"]
        away = game["away_team"]
        winner = game["winner"]

        for team in [home, away]:

            if team not in records:
                records[team] = {
                    "wins": 0,
                    "losses": 0,
                    "ties": 0
                }

        if winner == home:
            records[home]["wins"] += 1
            records[away]["losses"] += 1

        elif winner == away:
            records[away]["wins"] += 1
            records[home]["losses"] += 1

        elif winner is None:
            records[home]["ties"] += 1
            records[away]["ties"] += 1

        else:
            raise ValueError(f"Invalid winner: {winner}")

    return records


def strength_of_record(
    team,
    game_results,
    final_records,
    victories_only=False
):
    """
    Calculate strength of victory or strength of schedule.

    victories_only=True:
        Strength of victory

    victories_only=False:
        Strength of schedule

    Opponents are counted once per game played.
    """

    opponent_wins = 0
    opponent_losses = 0
    opponent_ties = 0

    for game in game_results:
        home = game["home_team"]
        away = game["away_team"]
        winner = game["winner"]

        if team == home:
            opponent = away

        elif team == away:
            opponent = home

        else:
            continue

        if victories_only and winner != team:
            continue

        record = final_records[opponent]

        opponent_wins += record["wins"]
        opponent_losses += record["losses"]
        opponent_ties += record["ties"]

    return winning_percentage(
        opponent_wins,
        opponent_losses,
        opponent_ties
    )


def two_team_division_tiebreaker(
    team_a,
    team_b,
    game_results,
    division_records,
    conference_records
):
    """
    Apply the first six NFL two-team division tiebreakers.

    Returns:
        winner: team abbreviation or None
        criterion: deciding tiebreaker
    """

    # 1. Head-to-head
    a_h2h = head_to_head_record(
        team_a, {team_b}, game_results
    )

    b_h2h = head_to_head_record(
        team_b, {team_a}, game_results
    )

    if a_h2h["pct"] > b_h2h["pct"]:
        return team_a, "head_to_head"

    if b_h2h["pct"] > a_h2h["pct"]:
        return team_b, "head_to_head"

    # 2. Division record
    a_div = division_records[team_a]
    b_div = division_records[team_b]

    a_pct = winning_percentage(
        a_div["wins"],
        a_div["losses"],
        a_div["ties"]
    )

    b_pct = winning_percentage(
        b_div["wins"],
        b_div["losses"],
        b_div["ties"]
    )

    if a_pct > b_pct:
        return team_a, "division_record"

    if b_pct > a_pct:
        return team_b, "division_record"

    # 3. Common games
    shared = common_opponents(
        team_a,
        team_b,
        game_results
    )

    a_common = common_games_record(
        team_a,
        shared,
        game_results
    )

    b_common = common_games_record(
        team_b,
        shared,
        game_results
    )

    if a_common["pct"] > b_common["pct"]:
        return team_a, "common_games"

    if b_common["pct"] > a_common["pct"]:
        return team_b, "common_games"

    # 4. Conference record
    a_conf = conference_records[team_a]
    b_conf = conference_records[team_b]

    a_pct = winning_percentage(
        a_conf["wins"],
        a_conf["losses"],
        a_conf["ties"]
    )

    b_pct = winning_percentage(
        b_conf["wins"],
        b_conf["losses"],
        b_conf["ties"]
    )

    if a_pct > b_pct:
        return team_a, "conference_record"

    if b_pct > a_pct:
        return team_b, "conference_record"

    # Reconstruct final records for SOV and SOS
    final_records = calculate_final_records(game_results)

    # 5. Strength of victory
    a_sov = strength_of_record(
        team_a,
        game_results,
        final_records,
        victories_only=True
    )

    b_sov = strength_of_record(
        team_b,
        game_results,
        final_records,
        victories_only=True
    )

    if a_sov > b_sov:
        return team_a, "strength_of_victory"

    if b_sov > a_sov:
        return team_b, "strength_of_victory"

    # 6. Strength of schedule
    a_sos = strength_of_record(
        team_a,
        game_results,
        final_records,
        victories_only=False
    )

    b_sos = strength_of_record(
        team_b,
        game_results,
        final_records,
        victories_only=False
    )

    if a_sos > b_sos:
        return team_a, "strength_of_schedule"

    if b_sos > a_sos:
        return team_b, "strength_of_schedule"

    return None, "unresolved"


def multi_team_head_to_head_records(
    teams,
    game_results
):
    """
    Calculate each team's record against all other
    teams involved in a multi-team tie.

    For division tiebreakers, the NFL compares the
    winning percentages in games among tied teams.
    """

    records = {}

    for team in teams:

        opponents = set(teams) - {team}

        records[team] = head_to_head_record(
            team,
            opponents,
            game_results
        )

    return records


def multi_team_head_to_head_sweep(
    teams,
    game_results
):
    """
    Identify head-to-head sweeps among tied teams.

    This helper is retained for future wild-card
    tiebreaking logic.

    It is NOT used for multi-team division tiebreakers.

    Returns:
        ("winner", team) if a team swept every other team
        ("eliminate", team) if a team lost every game
                            against every other team
        ("none", None) otherwise
    """

    pair_records = {}

    for team in teams:
        pair_records[team] = {}

        for opponent in teams:

            if opponent == team:
                continue

            pair_records[team][opponent] = head_to_head_record(
                team,
                {opponent},
                game_results
            )

    # Check for a team that swept all others
    for team in teams:

        if all(
            pair_records[team][opponent]["wins"] > 0
            and pair_records[team][opponent]["losses"] == 0
            and pair_records[team][opponent]["ties"] == 0
            for opponent in teams
            if opponent != team
        ):
            return "winner", team

    # Check for a team that lost to all others
    for team in teams:

        if all(
            pair_records[team][opponent]["losses"] > 0
            and pair_records[team][opponent]["wins"] == 0
            and pair_records[team][opponent]["ties"] == 0
            for opponent in teams
            if opponent != team
        ):
            return "eliminate", team

    return "none", None


def multi_team_division_tiebreaker(
    teams,
    game_results,
    division_records,
    conference_records
):
    """
    Apply the first six NFL multi-team division tiebreakers.

    If a multi-team tie is reduced to two teams,
    restart using the two-team procedure.

    If a four-team tie is reduced to three teams,
    restart using the three-team procedure.

    Returns:
        winner: team abbreviation or None
        criterion: deciding tiebreaker
    """

    if len(teams) < 2 or len(set(teams)) != len(teams):
        raise ValueError(
            "Provide at least two distinct teams."
        )

    if len(teams) == 2:
        return two_team_division_tiebreaker(
            teams[0],
            teams[1],
            game_results,
            division_records,
            conference_records
        )

    final_records = calculate_final_records(game_results)

    def resolve_scores(scores, criterion):
        """
        Compare teams at the current tiebreaking step.

        If one team remains, return that team.

        If two teams remain, restart the two-team
        tiebreaker from Step 1.

        If four teams are reduced to three, restart
        the three-team tiebreaker from Step 1.

        If all teams remain tied, continue to the
        next criterion.
        """

        best = max(scores.values())

        remaining = [
            team
            for team, value in scores.items()
            if value == best
        ]

        # One team wins the tiebreaker
        if len(remaining) == 1:
            return remaining[0], criterion, None

        # Restart with two teams
        if len(remaining) == 2:

            winner, two_team_criterion = (
                two_team_division_tiebreaker(
                    remaining[0],
                    remaining[1],
                    game_results,
                    division_records,
                    conference_records
                )
            )

            if winner is None:
                return None, "unresolved", None

            return (
                winner,
                f"restart_two_team_{two_team_criterion}",
                None
            )

        # Restart if four teams are reduced to three
        if len(teams) == 4 and len(remaining) == 3:

            winner, restart_criterion = (
                multi_team_division_tiebreaker(
                    remaining,
                    game_results,
                    division_records,
                    conference_records
                )
            )

            if winner is None:
                return None, "unresolved", None

            return (
                winner,
                f"restart_three_team_{restart_criterion}",
                None
            )

        # All teams remain tied
        return None, None, remaining

    # --------------------------------------------------
    # 1. Head-to-head among tied teams
    # --------------------------------------------------

    h2h = multi_team_head_to_head_records(
        teams,
        game_results
    )

    scores = {
        team: h2h[team]["pct"]
        for team in teams
    }

    winner, criterion, remaining = resolve_scores(
        scores,
        "multi_team_head_to_head"
    )

    if criterion is not None:
        return winner, criterion

    teams = remaining

    # --------------------------------------------------
    # 2. Division record
    # --------------------------------------------------

    scores = {
        team: winning_percentage(
            division_records[team]["wins"],
            division_records[team]["losses"],
            division_records[team]["ties"]
        )
        for team in teams
    }

    winner, criterion, remaining = resolve_scores(
        scores,
        "multi_team_division_record"
    )

    if criterion is not None:
        return winner, criterion

    teams = remaining

    # --------------------------------------------------
    # 3. Common games
    # --------------------------------------------------

    opponent_sets = []

    for team in teams:
        opponents = set()

        for game in game_results:

            if game["home_team"] == team:
                opponents.add(game["away_team"])

            elif game["away_team"] == team:
                opponents.add(game["home_team"])

        # Exclude the tied teams themselves
        opponents -= set(teams)

        opponent_sets.append(opponents)

    shared = set.intersection(*opponent_sets)

    scores = {
        team: common_games_record(
            team,
            shared,
            game_results
        )["pct"]
        for team in teams
    }

    winner, criterion, remaining = resolve_scores(
        scores,
        "multi_team_common_games"
    )

    if criterion is not None:
        return winner, criterion

    teams = remaining

    # --------------------------------------------------
    # 4. Conference record
    # --------------------------------------------------

    scores = {
        team: winning_percentage(
            conference_records[team]["wins"],
            conference_records[team]["losses"],
            conference_records[team]["ties"]
        )
        for team in teams
    }

    winner, criterion, remaining = resolve_scores(
        scores,
        "multi_team_conference_record"
    )

    if criterion is not None:
        return winner, criterion

    teams = remaining

    # --------------------------------------------------
    # 5. Strength of victory
    # --------------------------------------------------

    scores = {
        team: strength_of_record(
            team,
            game_results,
            final_records,
            victories_only=True
        )
        for team in teams
    }

    winner, criterion, remaining = resolve_scores(
        scores,
        "multi_team_strength_of_victory"
    )

    if criterion is not None:
        return winner, criterion

    teams = remaining

    # --------------------------------------------------
    # 6. Strength of schedule
    # --------------------------------------------------

    scores = {
        team: strength_of_record(
            team,
            game_results,
            final_records,
            victories_only=False
        )
        for team in teams
    }

    winner, criterion, remaining = resolve_scores(
        scores,
        "multi_team_strength_of_schedule"
    )

    if criterion is not None:
        return winner, criterion

    return None, "unresolved"


def select_division_winner(
    division_teams,
    final_records,
    game_results,
    division_records,
    conference_records
):
    """
    Select a division winner using overall record
    followed by NFL division tiebreakers.

    Returns:
        winner, deciding_criterion
    """

    # Calculate overall winning percentages
    percentages = {
        team: winning_percentage(
            final_records[team]["wins"],
            final_records[team]["losses"],
            final_records[team]["ties"]
        )
        for team in division_teams
    }

    best_pct = max(percentages.values())

    tied_teams = [
        team
        for team in division_teams
        if percentages[team] == best_pct
    ]

    # One team has the best overall record
    if len(tied_teams) == 1:
        return tied_teams[0], "overall_record"

    # Two teams are tied
    if len(tied_teams) == 2:
        return two_team_division_tiebreaker(
            tied_teams[0],
            tied_teams[1],
            game_results,
            division_records,
            conference_records
        )

    # Three or four teams are tied
    return multi_team_division_tiebreaker(
        tied_teams,
        game_results,
        division_records,
        conference_records
    )
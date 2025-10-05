import services.odd_calculator as od
from model.league import League


def handle_calculator(per_game, threshold, mode, house_odd):
    prob, fair_odd, house_edge = od.calculate_all(per_game, threshold, mode, house_odd)
    percent = prob * 100

    if house_edge:
        odd_info = {
            "probability_percent": round(percent, 2),
            "fair_odd": round(fair_odd, 2),
            "house_edge_percent": round(house_edge, 2),
        }
    else:
        odd_info = {
            "probability_percent": round(percent, 2),
            "fair_odd": round(fair_odd, 2),
        }
    return odd_info


def handle_team(
    league: League,
    team,
    stat,
    calculator_status: bool,
    threshold=None,
    mode=None,
    house_odd=None,
):
    league.df = league.by_team(team)

    total = None
    per_game = None

    if stat == "cards":
        total = league.total_cards_sum(team)
        per_game = league.total_cards_per_game(team)
    elif stat == "second half goals":
        total = league.goals_second_half_sum(team)
        per_game = league.goals_second_half_per_game(team)
    else:
        total = league.get_team_stat_sum(team, stat)
        per_game = league.get_team_stat_mean(team, stat)

    if calculator_status:
        odd_info = handle_calculator(per_game, threshold, mode, house_odd)
        response = {"per game": round(per_game, 2), "sum": int(total), "odd": odd_info}
    else:
        response = {"per game": round(per_game, 2), "sum": int(total)}

    return response


def handle_h2h(league: League, team1, team2, only_home=False, start_year=None, end_year=None):

    if league.name == "Brasileirao" and start_year and end_year:
        league.df = league.by_year(start_year, end_year)

    league.df = league.head_to_head(team1, team2, only_home)

    summary1 = league.get_result_summary(team1)
    summary2 = league.get_result_summary(team2)

    response = {
        team1: {"wins": summary1["W"], "losses": summary1["L"], "draws": summary1["D"]},
        team2: {"wins": summary2["W"], "losses": summary2["L"], "draws": summary2["D"]},
    }

    return response


def handle_league(league: League, stat, start_year=None, end_year=None):

    if league.name == "Brasileirao" and start_year and end_year:
        league.df = league.by_year(start_year, end_year)

    column_map = league.stat_map[stat]
    home_col = column_map["home"]
    away_col = column_map["away"]

    total = league.df[home_col].sum() + league.df[away_col].sum()
    per_game = league.df[home_col].mean() + league.df[away_col].mean()

    response = {"per_game": round(per_game, 2), "sum": int(total)}

    return response

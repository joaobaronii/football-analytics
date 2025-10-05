import pandas as pd

from .league import League


class Premier(League):
    # FTH/AG = full time home/away goals; FTR = full time result; HTH/AG = half time home/away goals; H/AS = home/away shots; H/AST = home/away shots on target;
    # H/AC = home/away corners; H/AF = H/A fouls committed; H/AY = H/A yellow cards; H/AR = H/A red cards
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)
        self.dataset_stats = [
            "FTHG",
            "FTAG",
            "HTHG",
            "HTAG",
            "HS",
            "AS",
            "HST",
            "AST",
            "HC",
            "AC",
            "HF",
            "AF",
            "HY",
            "AY",
            "HR",
            "AR",
        ]
        self.stat_map = {
            "goals": {"home": "FTHG", "away": "FTAG"},
            "ht_goals": {"home": "HTHG", "away": "HTAG"},
            "shots": {"home": "HS", "away": "AS"},
            "shots_on_target": {"home": "HST", "away": "AST"},
            "corners": {"home": "HC", "away": "AC"},
            "fouls": {"home": "HF", "away": "AF"},
            "yellow_cards": {"home": "HY", "away": "AY"},
            "red_cards": {"home": "HR", "away": "AR"},
        }
        self.name = "Premier League"

    def goals_second_half_sum(self, team):
        if team not in self.team_list:
            raise ValueError(
                "Team not in the dataset. Teams available: " + str(self.team_list)
            )

        ht_goals = self.get_team_stat_sum(team, "ht_goals")
        total_goals = self.get_team_stat_sum(team, "goals")

        second_half_goals = total_goals - ht_goals

        return second_half_goals

    def goals_second_half_per_game(self, team):
        total = self.goals_second_half_sum(team)

        games = self.get_games_played(team)

        return total / games

    def total_cards_sum(self, team):
        if team not in self.team_list:
            raise ValueError(
                "Team not in the dataset. Teams available: " + str(self.team_list)
            )

        yellow = self.get_team_stat_sum(team, "yellow_cards")
        red = self.get_team_stat_sum(team, "red_cards")
        total = yellow + red

        return total

    def total_cards_per_game(self, team):
        total = self.total_cards_sum(team)

        games = self.get_games_played(team)

        return total / games

import pandas as pd


class League:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.team_list = pd.concat([df["Home"], df["Away"]]).unique().tolist()
        self.dataset_stats = []
        self.stat_map = {}
        self.name = None

    def __repr__(self):
        return self.df.to_string()

    def by_team(self, team, only_home=False, only_away=False):
        if team not in self.team_list:
            raise ValueError("Team not in the dataset.")

        if only_home and only_away:
            raise ValueError(
                "Error: only_home and only_away is true. One(or both) of them must be false"
            )

        if only_home:
            filtered_df = self.df.loc[(self.df.Home == team)]
            return filtered_df
        if only_away:
            filtered_df = self.df.loc[(self.df.Away == team)]
            return filtered_df

        filtered_df = self.df.loc[(self.df.Home == team) | (self.df.Away == team)]
        return filtered_df

    def head_to_head(self, team1, team2, only_home=False):
        if team1 == team2:
            raise ValueError(f"{team1} X {team2}?")

        if team1 not in self.team_list or team2 not in self.team_list:
            raise ValueError(
                "Team not in the dataset. Teams available: " + str(self.team_list)
            )

        if only_home:
            filtered_df = self.df.loc[(self.df.Home == team1) & (self.df.Away == team2)]
            return filtered_df

        check = [team1, team2]
        filtered_df = self.df.loc[
            (self.df.Home.isin(check)) & (self.df.Away.isin(check))
        ]
        return filtered_df

    def get_stat_mean(self, stat):
        if stat not in self.dataset_stats:
            raise ValueError(
                "Stat not in the dataset. Stats available: " + str(self.dataset_stats)
            )

        return self.df[stat].mean()

    def get_stat_sum(self, stat):
        if stat not in self.dataset_stats:
            raise ValueError(
                "Stat not in the dataset. Stats available: " + str(self.dataset_stats)
            )

        return self.df[stat].sum()

    def get_result_summary(self, team):
        if team not in self.team_list:
            raise ValueError(
                "Team not in the dataset. Teams available: " + str(self.team_list)
            )

        win_sum = (
            ((self.df.Home == team) & (self.df.FTR == "H"))
            | ((self.df.Away == team) & (self.df.FTR == "A"))
        ).sum()
        loss_sum = (
            ((self.df.Home == team) & (self.df.FTR == "A"))
            | ((self.df.Away == team) & (self.df.FTR == "H"))
        ).sum()
        draw_sum = (
            ((self.df.Home == team) | (self.df.Away == team)) & (self.df["FTR"] == "D")
        ).sum()

        results = {"W": int(win_sum), "L": int(loss_sum), "D": int((draw_sum))}
        return results

    def get_total_stat_sum(self, team, stat):
        if stat not in self.stat_map:
            raise ValueError(
                "Stat not in the dataset. Stats available: "
                + str(list(self.stat_map.keys()))
            )

        if team not in self.team_list:
            raise ValueError(
                "Team not in the dataset. Teams available: " + str(self.team_list)
            )

        column_map = self.stat_map[stat]
        home_col = column_map["home"]
        away_col = column_map["away"]

        at_home = self.df.loc[self.df.Home == team, home_col].sum()
        away = self.df.loc[self.df.Away == team, away_col].sum()

        return at_home + away

    def get_games_played(self, team):
        games_played = len(((self.df.Home == team) | (self.df.Away == team)))
        if games_played == 0:
            return 0

        return games_played

    def get_total_stat_mean(self, team, stat):
        total = self.get_total_stat_sum(team, stat)

        games = self.get_games_played(team)

        return total / games

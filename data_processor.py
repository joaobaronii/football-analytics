import pandas as pd
from data_loader import load_premier_league_2025


# TODO número de gol(casa, visitante, total); retrospecto confronto; campanha no ano; jogos do time no dia X; 

class League:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.team_list = pd.concat([df['Home'], df['Away']]).unique().tolist()

    def __repr__(self):
        return self.df.to_string()
    
    def by_team(self, team, only_home=False, only_away=False):
        if team not in self.team_list:
            raise ValueError("Team not in the dataset.")
        
        if only_home and only_away:
            raise ValueError("Error: only_home and only_away is true. One(or both) of them must be false")

        if only_home:
            filtered_df = self.df.loc[(self.df.Home == team)]
            return self.__class__(filtered_df)
        if only_away:
            filtered_df = self.df.loc[(self.df.Away == team)]
            return self.__class__(filtered_df)
        
        filtered_df = self.df.loc[(self.df.Home == team) | (self.df.Away == team)]
        return self.__class__(filtered_df)
    


    def head_to_head(self, team1, team2, only_home=False):
        if team1 == team2:
            raise ValueError(f"{team1} X {team2}?")
        
        if team1 not in self.team_list or team2 not in self.team_list:
            raise ValueError("Team not in the dataset.")
        
        if only_home:
            filtered_df = self.df.loc[(self.df.Home == team1) & (self.df.Away == team2)]
            return self.__class__(filtered_df)
        
        check = [team1, team2]
        filtered_df = self.df.loc[(self.df.Home.isin(check)) & (self.df.Away.isin(check))]
        return self.__class__(filtered_df)
    

class Brasileirao(League):
    def by_year(self, year): 
        filtered_df = self.df.loc[(self.df.Season == year)]
        return Brasileirao(filtered_df)


class Premier(League):
    # FTH/AG = full time home/away goals; FTR = full time result; HTH/AG = half time home/away goals; H/AS = home/away shots; H/AST = home/away shots on target;
    # H/AC = home/away corners; H/AF = H/A fouls committed; H/AY = H/A yellow cards; H/AR = H/A red cards
    stats_for_functions = ["FTHG", "FTAG", "HTHG", "HTAG", "HS", "AS", "HST", "AST", "HC", "AC", "HF", "AF", "HY", "AY", "HR", "AR"]

    def get_stat_mean(self, stat):
        if stat not in Premier.stats_for_functions:
            raise ValueError("Stat not in the dataset.")
        
        return self.df[stat].mean()
        
    def get_stat_sum(self, stat):
        if stat not in Premier.stats_for_functions:
            raise ValueError("Stat not in the dataset.")
        
        return self.df[stat].sum()

    

if __name__ == "__main__":
    df = Premier(load_premier_league_2025())
    df = df.by_team("Arsenal", only_home=True, only_away=False)

    print(df)
    mean = df.get_stat_mean("HS")
    soma = df.get_stat_sum("HS")

    print(mean, soma)
    print(df.team_list)



import pandas as pd
from data_loader import load_brasileirao

class Brasileirao:
    def __init__(self, df):
        self.df = df
        self.team_list = df["Home"].unique().tolist()

    
    def __repr__(self):
        return self.df.to_string()

    def by_year(self, year): 
        filtered_df = self.df.loc[year]
        return Brasileirao(filtered_df)

    def head_to_head(self, team1, team2, only_home=False):
        if team1 == team2:
            raise ValueError(f"{team1} X {team2}?")
        
        if team1 not in self.team_list or team2 not in self.team_list:
            raise ValueError(f"Team not in the dataset.")
        
        if only_home:
            filtered_df = self.df.loc[(self.df.Home == team1) & (self.df.Away == team2)]
            return Brasileirao(filtered_df)
        
        check = [team1, team2]
        filtered_df = self.df.loc[(self.df.Home.isin(check)) & (self.df.Away.isin(check))]
        return Brasileirao(filtered_df)


if __name__ == "__main__":
    df = Brasileirao(load_brasileirao())
    print(df.team_list)
    df = df.by_year(2023)
    df = df.head_to_head("Corinthians", "Cruzeiro")

    print(df)
    print(df.team_list)



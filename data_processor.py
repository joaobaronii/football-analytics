import pandas as pd
from data_loader import load_brasileirao


TEAM_LIST_BRASILEIRAO = ['Palmeiras', 'Sport Recife', 'Figueirense', 'Botafogo RJ', 'Corinthians', 'Internacional', 'Ponte Preta', 'Bahia', 'Cruzeiro', 'Vasco', 'Atletico GO', 'Flamengo RJ', 'Portuguesa', 'Nautico', 'Atletico-MG', 'Coritiba', 'Santos', 'Sao Paulo', 'Fluminense', 'Gremio', 'Vitoria', 'Criciuma', 'Athletico-PR', 'Goias', 'Chapecoense-SC', 'Avai', 'Joinville', 'Santa Cruz', 'America MG', 'Parana', 'Ceara', 'CSA', 'Fortaleza', 'Bragantino', 'Cuiaba', 'Juventude', 'Mirassol']

class Brasileirao:
    def __init__(self, df):
        self.df = df
    
    def __repr__(self):
        return self.df.to_string()

    def by_year(self, year): 
        filtered_df = self.df.loc[year]
        return Brasileirao(filtered_df)

    def head_to_head(self, team1, team2, only_home=False):
        if team1 == team2:
            raise ValueError(f"{team1} X {team2}?")
        
        if team1 not in TEAM_LIST_BRASILEIRAO or team2 not in TEAM_LIST_BRASILEIRAO:
            raise ValueError(f"Team not in the dataset.")
        
        if only_home:
            filtered_df = self.df.loc[(self.df.Home == team1) & (self.df.Away == team2)]
            return Brasileirao(filtered_df)
        
        check = [team1, team2]
        filtered_df = self.df.loc[(self.df.Home.isin(check)) & (self.df.Away.isin(check))]
        return Brasileirao(filtered_df)


if __name__ == "__main__":
    df = Brasileirao(load_brasileirao())
    df = df.by_year(2023)
    df = df.head_to_head("Corinthians", "Cruzeiro")

    print(df)


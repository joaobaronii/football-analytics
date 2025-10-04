import pandas as pd
from .league import League


class Brasileirao(League):
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)
        self.dataset_stats = ["HG", "AG"]
        self.stat_map = {"goals": {"home": "HG", "away": "AG"}}
        self.name = "Brasileirao"

    def by_year(self, year1, year2=None):
        if year2 == None:
            filtered_df = self.df.loc[(self.df.Season == year1)]
            return filtered_df
        
        filtered_df = self.df[self.df.Season.between(year1, year2)]
        return filtered_df
        

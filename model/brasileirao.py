import pandas as pd
from .league import League


class Brasileirao(League):
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)
        self.dataset_stats = ["HG", "AG"]
        self.stat_map = {"goals": {"home": "HG", "away": "AG"}}

    def by_year(self, year):
        filtered_df = self.df.loc[(self.df.Season == year)]
        return Brasileirao(filtered_df)

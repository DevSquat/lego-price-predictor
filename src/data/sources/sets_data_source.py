import pandas as pd
from .base_source import DataSource
from src.project_paths import get_in_project

class SetsDataSource(DataSource):

    def load(self):
        df = pd.read_csv(get_in_project("data", "raw", "rebrickable", "sets.csv"),
                         usecols=["set_num","year","theme_id","num_parts"])
        return df

    def normalize(self, df):
        return df

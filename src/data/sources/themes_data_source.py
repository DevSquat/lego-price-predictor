import pandas as pd
from .base_source import DataSource
from src.project_paths import get_in_project

class ThemesDataSource(DataSource):

    def load(self):
        df = pd.read_csv(
            get_in_project("data", "raw", "rebrickable", "themes.csv"),
            usecols=['theme_id','name'])
        return df

    def normalize(self, df):
        return df

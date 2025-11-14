import pandas as pd
from .base_source import DataSource
from src.project_paths import get_in_project

class InventoriesDataSource(DataSource):

    def load(self):
        df = pd.read_csv(
            get_in_project("data", "raw", "rebrickable", "inventories.csv"),
            usecols=['id','set_num'])
        return df

    def normalize(self, df):
        return df

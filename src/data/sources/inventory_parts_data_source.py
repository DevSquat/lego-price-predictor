import pandas as pd
from .base_source import DataSource
from src.project_paths import get_in_project

class InventoryPartsDataSource(DataSource):

    def load(self):
        df = pd.read_csv(get_in_project("data", "raw", "rebrickable", "inventory_parts.csv"),
                         usecols=['inventory_id','part_num'])
        return df

    def normalize(self, df):
        return df

import pandas as pd
from .base_source import DataSource
from src.project_paths import get_in_project

class InventoriesDataSource(DataSource):

    def load(self):
        price_data = pd.read_excel(get_in_project("data", "raw", "used_prices", "lego_final_data.xlsx"),
                                   usecols=['number', 'numberVariant', 'US_retailPrice', 'US_dateFirstAvailable',
                                            'US_dateLastAvailable', 'PL_retailPrice', 'Date', 'PriceMonthPLN'])

        price_data['set_id'] = price_data['number'].astype(str) + '-' + price_data['numberVariant'].astype(str)
        price_data = price_data.drop(['number', 'numberVariant'], axis=1)
        return price_data

    def normalize(self, df):
        return df

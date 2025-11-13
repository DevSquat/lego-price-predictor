from pathlib import Path

import pandas as pd
from .base_source import DataSource
from src.project_paths import get_in_project

def min_max_scale(series):
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        return series.apply(lambda x: 0.0)
    return (series - min_val) / (max_val - min_val)


class ThemesTrendingScoreDataSource(DataSource):

    def load(self):
        df = self.merge_scraped_data()
        return df


    def normalize(self, df):
        summary_rows = []

        for col in df.columns:
            series = pd.to_numeric(df[col], errors='coerce')

            non_zero_idx = series.ne(0) & series.notna()
            if not non_zero_idx.any():
                continue  # Skip if column has only 0s or NaNs

            first_valid_index = non_zero_idx.idxmax()
            trimmed_series = series.loc[first_valid_index:].dropna()

            max_val = trimmed_series.max()
            avg_val = trimmed_series.mean()

            summary_rows.append({
                'set_id': col,
                'maximum_value': max_val,
                'avg': avg_val
            })

            # Create summary dataframe
        summary_df = pd.DataFrame(summary_rows)

        # Save results to new CSV
        summary_df['maximum_value'] = min_max_scale(summary_df['maximum_value'])
        summary_df['avg'] = min_max_scale(summary_df['avg'])
        return df

    def merge_scraped_data(self):

        result_df = pd.DataFrame()
        base_path = get_in_project("data", "raw", "google_trends")

        for csv_path in base_path.rglob("*.csv"):
            parts = csv_path.stem.split("_")
            if len(parts) < 1:
                continue
            df = pd.read_csv(csv_path, skiprows=3, header=None)

            column_names = ['date', 'barbie'] + parts
            df.columns = column_names[:df.shape[1]]

            numeric_cols = df.columns.difference(['date'])
            df[numeric_cols] = df[numeric_cols].applymap(lambda x: 0.01 if x == '<1' else x)

            barbie_row = df[df['date'] == '2005-12']
            if not barbie_row.empty:
                try:
                    barbie_val = float(barbie_row.iloc[0]['barbie'])
                    multiplier = 100 / barbie_val
                    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce') * multiplier
                    extra_cols = df.columns.difference(['date', 'barbie'])
                    result_df = pd.concat([result_df, df[extra_cols]], axis=1)
                except Exception:
                    continue
            else:
                continue

        return result_df
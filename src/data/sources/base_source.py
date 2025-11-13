from abc import ABC, abstractmethod
import pandas as pd

class DataSource(ABC):
    @abstractmethod
    def load(self) -> pd.DataFrame:
        """Load raw data from disk or API"""
        pass

    @abstractmethod
    def normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names, formats, units, etc."""
        pass

import numpy as np
import pandas as pd
import pandas as pd

class DataCleaner:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def clean_data(self):
        try:
            # Count total missing values per row before cleaning
            initial_missing = self.dataframe.isnull().sum(axis=1)
            num_initial_missing_rows = (initial_missing > 0).sum()
            print(f"Number of rows with missing data before cleaning: {num_initial_missing_rows}")

            # Drop rows with any missing values
            cleaned_dataframe = self.dataframe.dropna()

            # Count total missing values per row after cleaning
            final_missing = cleaned_dataframe.isnull().sum(axis=1)
            num_final_missing_rows = (final_missing > 0).sum()
            print(f"Number of rows with missing data after cleaning: {num_final_missing_rows}")

            # Calculate and print the number of missing rows cleaned
            num_rows_cleaned = num_initial_missing_rows - num_final_missing_rows
            print(f"Number of missing rows removed: {num_rows_cleaned}")

            return cleaned_dataframe
        except Exception as e:
            print(f"Error cleaning data: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on error



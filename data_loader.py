import pandas as pd
from Weather import Weather

class DataLoader:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def load_data(self):
        try:
            # Read the CSV file
            df = pd.read_csv(self.csv_file)

            # Convert temperature from Kelvin to Fahrenheit and round to the nearest tenth
            df['temperature'] = round((df['temperature'] - 273.15) * 9 / 5 + 32, 1)
            
            # Create Weather objects from DataFrame rows
            weather_data = [
                Weather(
                    row['datetime'], 
                    row['wind_speed'], 
                    row['wind_direction'], 
                    row['pressure'], 
                    row['humidity'], 
                    row['temperature'], 
                    pd.to_datetime(row['datetime']).hour,  # Extracting hour
                    pd.to_datetime(row['datetime']).day,   # Extracting day of the month
                    pd.to_datetime(row['datetime']).month  # Extracting month
                ) for index, row in df.iterrows()
            ]
            return weather_data
        except Exception as e:
            print(f"Error loading data: {e}")
            return []



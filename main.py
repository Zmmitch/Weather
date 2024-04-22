from data_loader import DataLoader
from data_cleaner import DataCleaner
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from VAR import VARModel  # Ensure this is defined and imported
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

def weather_to_dataframe(weather_data):
    return pd.DataFrame([vars(w) for w in weather_data])

if __name__ == "__main__":
    data_loader = DataLoader('weather_data.csv')
    weather_data = data_loader.load_data()
    weather_df = weather_to_dataframe(weather_data)

    data_cleaner = DataCleaner(weather_df)
    cleaned_weather_df = data_cleaner.clean_data()

    # Ensure the datetime column is properly converted and set as index
    if 'datetime' in cleaned_weather_df.columns:
        cleaned_weather_df['datetime'] = pd.to_datetime(cleaned_weather_df['datetime'])
        cleaned_weather_df.set_index('datetime', inplace=True)

    train_data, test_data = train_test_split(cleaned_weather_df, test_size=0.2, shuffle=False)

    # Assuming VAR model uses only numeric data
    train_data_numeric = train_data.select_dtypes(include=[np.number])
    test_data_numeric = test_data.select_dtypes(include=[np.number])

    var_model = VARModel(train_data_numeric)
    var_model.fit()
    print(var_model.summary())

    forecast_steps = len(test_data_numeric)
    forecasted_values = var_model.forecast(steps=forecast_steps)

    # Convert forecasted values to DataFrame
    forecast_index = pd.date_range(start=train_data.index[-1], periods=forecast_steps, freq='h')  # Adjust freq accordingly
    forecast_df = pd.DataFrame(forecasted_values, index=forecast_index, columns=train_data_numeric.columns)

    # Plotting the forecast against actual data for 'temperature' as an example
    plt.figure(figsize=(10, 5))
    plt.plot(test_data_numeric.index, test_data_numeric['humidity'], label='Actual Humidity')
    plt.plot(forecast_df.index, forecast_df['humidity'], label='Forecasted Temperature', linestyle='--')
    plt.title('humidity Forecast vs Actuals')
    plt.xlabel('Date')
    plt.ylabel('Humidity')
    plt.legend()
    plt.show()

    # Calculate and print the Mean Squared Error for temperature
    mse = mean_squared_error(test_data_numeric['temperature'], forecast_df['temperature'])
    print(f"Mean Squared Error for Temperature Forecast: {mse}")
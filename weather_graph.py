import matplotlib.pyplot as plt
import pandas as pd
from data_loader import DataLoader
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
class WeatherGraph:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def plot_temperature(self):
        timestamps = [weather.datetime for weather in self.weather_data]
        temperatures = [weather.temperature for weather in self.weather_data]
        
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, temperatures, color='red')
        plt.xlabel('Timestamp')
        plt.ylabel('Temperature (°C)')
        plt.title('Temperature Over Time')
        plt.grid(True)
        plt.show()

    def plot_humidity(self):
        timestamps = [weather.datetime for weather in self.weather_data]
        humidity = [weather.humidity for weather in self.weather_data]
        
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, humidity, color='blue')
        plt.xlabel('Timestamp')
        plt.ylabel('Humidity (%)')
        plt.title('Humidity Over Time')
        plt.grid(True)
        plt.show()
           
        result = adfuller(self)
        print('ADF Statistic: %f' % result[0])
        print('p-value: %f' % result[1])

    def summary_statistics(self):
        temperature_summary = [weather.temperature for weather in self.weather_data]
        humidity_summary = [weather.humidity for weather in self.weather_data]
        wind_speed_summary = [weather.wind_speed for weather in self.weather_data]
        wind_direction_summary = [weather.wind_direction for weather in self.weather_data]
        pressure_summary = [weather.pressure for weather in self.weather_data]

        print("Temperature Summary:")
        print(pd.Series(temperature_summary).describe())
        print("\nHumidity Summary:")
        print(pd.Series(humidity_summary).describe())
        print("\nWind Speed Summary:")
        print(pd.Series(wind_speed_summary).describe())
        print("\nWind Direction Summary:")
        print(pd.Series(wind_direction_summary).describe())
        print("\nPressure Summary:")
        print(pd.Series(pressure_summary).describe())

    def plot_line_plots(self):
        timestamps = pd.to_datetime([weather.datetime for weather in self.weather_data])
        wind_speed = [weather.wind_speed for weather in self.weather_data]
        wind_direction = [weather.wind_direction for weather in self.weather_data]
        pressure = [weather.pressure for weather in self.weather_data]
        humidity = [weather.humidity for weather in self.weather_data]
        temperature = [weather.temperature for weather in self.weather_data]
        
        fig, axs = plt.subplots(5, 1, figsize=(12, 18))
        axs[0].plot(timestamps, wind_speed, color='blue')
        axs[0].set_ylabel('Wind Speed')
        axs[1].plot(timestamps, wind_direction, color='green')
        axs[1].set_ylabel('Wind Direction')
        axs[2].plot(timestamps, pressure, color='red')
        axs[2].set_ylabel('Pressure')
        axs[3].plot(timestamps, humidity, color='orange')
        axs[3].set_ylabel('Humidity')
        axs[4].plot(timestamps, temperature, color='purple')
        axs[4].set_ylabel('Temperature')
        for ax in axs:
            ax.grid(True)
        plt.xlabel('Timestamp')
        plt.show()

    def plot_seasonal_decomposition(self, variable):
        timestamps = pd.to_datetime([weather.datetime for weather in self.weather_data])
        data = [getattr(weather, variable) for weather in self.weather_data]

        
        mean = np.nanmean(data)
        data = [x if not np.isnan(x) else mean for x in data]

    # Plot seasonal decomposition

        # Create a DataFrame with timestamps and data
        df = pd.DataFrame({variable: data}, index=timestamps)
        
        # Drop missing values
        
        df = df.dropna()  
        print(data[:10])
        result = seasonal_decompose(df[variable], model='additive', period=24)  # Assuming hourly data
        
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 10))
        ax1.plot(df.index, df[variable], label='Original', color='blue')
        ax1.legend(loc='upper left')
        ax2.plot(df.index, result.trend, label='Trend', color='red')
        ax2.legend(loc='upper left')
        ax3.plot(df.index, result.seasonal, label='Seasonal', color='green')
        ax3.legend(loc='upper left')
        ax4.plot(df.index, result.resid, label='Residual', color='purple')
        ax4.legend(loc='upper left')
        plt.xlabel('Timestamp')
        plt.suptitle('Seasonal Decomposition - ' + variable)

        plt.subplots_adjust(hspace=0.5)
        plt.show()

    def plot_weather_description(self):

        timestamps = pd.to_datetime([weather.datetime for weather in self.weather_data])
        weather_description = [weather.weather_description for weather in self.weather_data]

        plt.figure(figsize=(12, 6))
        plt.bar(timestamps, weather_description, color='skyblue')
        plt.xlabel('Timestamp')
        plt.ylabel('Weather Description')
        plt.title('Weather Description Over Time')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
# Test the WeatherGraph class

if __name__ == "__main__":
    # Assume weather_data is a list of Weather objects
    data_loader = DataLoader('weather_data.csv')
    weather_data = data_loader.load_data()

 
    # weather_graph = WeatherGraph(weather_data)
    # weather_graph.plot_temperature()
    # weather_graph.plot_humidity()
    weather_graph = WeatherGraph(weather_data)
    # weather_graph.plot_line_plots()
    # weather_graph.plot_seasonal_decomposition('temperature')
    weather_graph.plot_weather_description()



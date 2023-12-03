import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from simulator_api.timeseries.seasonality import calculate_seasonality
from simulator_api.timeseries.trend import Trend
from simulator_api.timeseries.edit_data import EditData
from simulator_api.timeseries.configuration_manager import DatasetConfigurationManager


class TimeSeries:
    """
    A class for generating time series data based on configuration settings.

    Args:
        config (ConfigurationManager): An instance of ConfigurationManager for accessing configuration data.

    Attributes:
        config (ConfigurationManager): An instance of ConfigurationManager containing configuration settings.

    Methods:
        _generate_time_series(): Generate the date-time index for the time series data.
        generate_data(): Generate the time series data based on seasonality and trend components.
    """

    def __init__(self, start_date, end_date, data_types, data_size, dataset):
        dataset= DatasetConfigurationManager(dataset)
        self.start_date = start_date
        self.end_date = end_date
        self.data_size = data_size
        self.data_types = data_types
        self.frequencies = dataset.get_frequency()
        self.trend_coefficients = dataset.get_trend_coefficient()
        self.cycle_amplitude = dataset.get_cycle_amplitude()
        self.cycle_frequency = dataset.get_cycle_frequency()
        self.missing_percentage = dataset.get_missing_percentage()
        self.outlier_percentage = dataset.get_outlier_percentage()
        self.noise_level = dataset.get_noise_level()
        self.seasonality_components= dataset.get_seasonality_components()


    def _generate_time_series(self):
        """
        Generate the date-time index for the time series data.

        Returns:
            pandas.DatetimeIndex: A date-time index based on the configuration settings.
        """
        # if the request has no end date, generate the time series data based on the data size
        if self.end_date:
            return pd.date_range(start=self.start_date, end=self.end_date, freq=self.frequencies)
        else:
            return pd.date_range(start=self.start_date, periods=self.data_size, freq=self.frequencies)

    def _transform_data(self, data):
        """
        Transform the data to be in range (-1,1)

        Return:
            pands.Series :data after transformation
        """
        scaler = MinMaxScaler(feature_range=(-1, 1))
        # Transform the data to be in the range between -1 and 1
        data = scaler.fit_transform(data.values.reshape(-1, 1))
        # after transformation get data to time series
        data = pd.Series(np.concatenate(data))

        return data
    def generate_data(self):
        """
        Generate the time series data based on seasonality and trend components.

        Returns:
            tuple: A tuple containing the generated time series data and the corresponding date-time index.
        """
        date_time_series = self._generate_time_series()
        data_size=len(date_time_series)
        component = np.zeros(data_size) if self.data_types == 'additive' else np.ones(data_size)
        if self.data_types == 'additive':
            component += self.cycle_amplitude * np.sin(self.cycle_frequency* (date_time_series.dayofyear/365))
            component += Trend(data_size,self.data_types,self.trend_coefficients).component()
        else:
            component *= self.cycle_amplitude * np.sin(self.cycle_frequency* (date_time_series.dayofyear/365))
            component *= Trend(data_size,self.data_types,self.trend_coefficients).component()

        # Iterate through Seasonality components
        for seasonality_component in self.seasonality_components:
            if self.data_types == 'additive':
                # data_size, series_type, data
                component += calculate_seasonality(date_time_series,self.data_types,seasonality_component)
            else:
                component *= calculate_seasonality(date_time_series,self.data_types,seasonality_component)

        # Iterate through the trend coefficients in reverse order
        data = self._transform_data(component)
        data, anomaly_mask = EditData(data,self.missing_percentage,self.noise_level,self.outlier_percentage).apply()
        return date_time_series,data, anomaly_mask



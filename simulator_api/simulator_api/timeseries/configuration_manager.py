import yaml
from dotenv import dotenv_values
from datetime import datetime
import json


class ConfigurationManager():

    def __init__(self, json):
        self.json = json

class SimulatorConfigurationManager(ConfigurationManager):

    def get_name(self):
        """
        Get the name of the simulator.
        Returns:
            str: The name of the simulator.
        """
        return self.json['name']

    def get_start_date(self):
        """
        Get the start date as a datetime object.

        Returns:
            datetime: The start date.
        """
        return self.json['start_date']

    def get_end_date(self):
        """
        Get the start date as a datetime object.

        Returns:
            datetime: The end date.
         """
        return self.json['end_date']

    def get_data_size(self):
        """
        Get the data size.

        Returns:
            int: The data size.
        """
        return self.json['data_size']

    def get_series_type(self):
        """
        Get series type for the time series.

        Returns:
            str: 'additive' or 'multiplicative'
        """
        return self.json['series_type']

    def get_producer_type(self):
        """
        Get producer type for the time series.

        Returns:
            str: 'kafka' or 'csv'
        """
        return self.json['producer_type']

    def get_datasets(self):
        """
        Get datasets for the time series.

        Returns:
            list: list of datasets
        """
        return self.json['data']


class DatasetConfigurationManager(ConfigurationManager):

    def get_cycle_amplitude(self):
        """
        Get cycle amplitude for the dataset.

        Returns:
            int: 0 for additive, 1 for multiplicative
        """
        return self.json['cycle_amplitude']

    def get_cycle_frequency(self):
        """
        Get cycle frequency for the dataset.

        Returns:
            float: cycle frequency
        """
        return self.json['cycle_frequency']

    def get_frequency(self):
        """
        Get frequency for the dataset.

        Returns:
            str: frequency
        """
        return self.json['frequency']

    def get_noise_level(self):
        """
        Get noise level for the dataset.

        Returns:
            float: noise level
        """
        return self.json['noise_level']

    def get_trend_coefficient(self):
        """
        Get trend coefficient for the dataset.

        Returns:
            list: trend coefficient
        """
        return self.json['trend_coefficient']


    def get_seasonality_components(self):
        """
        Get seasonality components for the dataset.

        Returns:
            list: seasonality components
        """
        return self.json['seasonality_components']

    def get_missing_percentage(self):
        """
        Get missing percentage for the dataset.

        Returns:
            float: missing percentage
        """
        return self.json['missing_percentage']

    def get_outlier_percentage(self):
        """
        Get outlier percentage for the dataset.

        Returns:
            float: outlier percentage
        """
        return self.json['outlier_percentage']


class SeasonalityConfigurationManager(ConfigurationManager):

    def get_frequency_type(self):
        """
        Get frequency type for the seasonality.

        Returns:
            str: frequency type
        """
        return self.json['frequency_type']

    def get_amplitude(self):
        """
        Get amplitude for the seasonality.

        Returns:
            float: amplitude
        """
        return self.json['amplitude']

    def get_phase_shift(self):
        """
        Get phase shift for the seasonality.

        Returns:
            float: phase shift
        """
        return self.json['phase_shift']

    def get_frequency_multiplier(self):
        """
        Get frequency multiplier for the seasonality.

        Returns:
            float: frequency multiplier
        """
        return self.json['frequency_multiplier']
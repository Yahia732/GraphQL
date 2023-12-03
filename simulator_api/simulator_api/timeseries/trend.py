import numpy as np
import pandas as pd


class Trend:
    """
    A class for modeling the trend component in time series data.

    Args:
        config (ConfigurationManager): An instance of ConfigurationManager for accessing configuration data.
        data (DatetimeIndex): The time series data.

    Attributes:
        data_size (int): The number of days in the time series data.
        trend_coefficients (list): Coefficients for trend components (default is [0, 0, 0]).
        series_type (str): The data type configuration from the ConfigurationManager ('additive' or 'multiplicative').

    Methods:
        component(): Calculate the trend component for the given time series data.
    """

    def __init__(self,data_size ,series_type, trend_coefficients : list):

        self.data_size = data_size
        self.trend_coefficients = trend_coefficients
        self.data_type = series_type

    def component(self):
        # return values follow equation trend_coefficient[i] * x^2 +trend_cofficient[i+1] *x +trend coefficient[1]
        # with length equal to datasize
        component = np.zeros(self.data_size) if self.data_type == 'additive' else np.ones(self.data_size)

        # Iterate through the trend coefficients in reverse order
        for i, coefficient in enumerate(reversed(self.trend_coefficients)):
            power = len(self.trend_coefficients) - 1 - i  # Calculate the exponent

            # Calculate the trend values for each data point
            component += coefficient * (np.arange(self.data_size) ** power)

        return pd.Series(component)

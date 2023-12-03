import numpy as np
import pandas as pd


class EditData:
    """
    A class for editing time series data by adding missing values, noise, and outliers based on configuration settings.

    Args:
        config (ConfigurationManager): An instance of ConfigurationManager for accessing configuration data.
        data (pandas.Series): The time series data to be edited.

    Attributes:
        data (pandas.Series): The time series data to be edited.
        percentage_missing (float): The percentage of missing values to be added to the data.
        noise_level (str): The noise level configuration from the ConfigurationManager ('small', 'large', or 'no_noise').
        percentage_outliers (float): The percentage of outliers to be added to the data.

    Methods:
        add_missing_values(): Add missing values to the time series data.
        add_noise(): Add noise to the time series data based on the noise level configuration.
        add_outliers(): Add outliers to the time series data.
        apply(): Apply the data editing operations and return the edited data along with an anomaly mask.
    """

    def __init__(self,data, percentage_missing, noise_level, percentage_outliers):
        self.data = data
        self.percentage_missing = percentage_missing
        self.noise_level = noise_level
        self.percentage_outliers = percentage_outliers

    def add_missing_values(self):
        """
        Add missing values to the time series data.

        Returns:
            None
        """
        num_missing = int(len(self.data) * self.percentage_missing)
        missing_indices = np.random.choice(len(self.data), size=num_missing, replace=False)
        self.data[missing_indices] = np.nan

    def add_noise(self):
        """
        Add noise to the time series data based on the noise level configuration.

        Returns:
            None
        """

        noise = np.zeros_like(self.data)
        for i in range(len(self.data)):
            # Get the noise from a normal distribution with mean 0 and std abs(self.data[i]) * noise_level
            noise[i] = np.random.normal(loc=0, scale=abs(self.data[i]) * self.noise_level) if self.noise_level > 0 else 0
        self.data = self.data + pd.Series(noise)

    def add_outliers(self):
        """
        Add outliers to the time series data.

        Returns:
            numpy.ndarray: An anomaly mask indicating the positions of added outliers.
        """
        num_outliers = int(len(self.data) * self.percentage_outliers)
        outlier_indices = np.random.choice(len(self.data), size=num_outliers, replace=False)
        # The outlier is 1 or -1 and replace with true data
        outliers = np.random.uniform(-1, 1, num_outliers)
        anomaly_mask = np.zeros(len(self.data), dtype=bool)
        if len(outliers) > 0:
            self.data[outlier_indices] = outliers
            anomaly_mask[outlier_indices] = True
        return anomaly_mask

    def apply(self):
        """
        Apply the data editing operations and return the edited data along with an anomaly mask.

        Returns:
            tuple: A tuple containing the edited data and an anomaly mask.
        """
        self.add_noise()
        anomaly_mask = self.add_outliers()
        self.add_missing_values()
        return self.data, anomaly_mask

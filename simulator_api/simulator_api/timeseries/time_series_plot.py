import matplotlib.pyplot as plt
import pandas as pd


class TimeSeriesPlotter:
    def __init__(self, date_rng: pd.DatetimeIndex, data: pd.Series):
        self.date_rng = date_rng
        self.data = data

    def plot(self):
        plt.figure(figsize=(10, 6))
        # Plot the time series data
        plt.plot(self.date_rng, self.data, marker='o', linestyle='-', color='b',
                 label='Time Series Data')
        # Add labels and title
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title('Time Series Plot')
        plt.legend()
        # Display the plot
        plt.tight_layout()
        plt.show()
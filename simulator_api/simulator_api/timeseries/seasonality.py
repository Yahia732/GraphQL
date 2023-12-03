import numpy as np
import pandas as pd
from abc import abstractmethod
from simulator_api.timeseries.configuration_manager import SeasonalityConfigurationManager


class Seasonality:
    def __init__(self, seasonality_component : SeasonalityConfigurationManager):
        self.frequency_type = seasonality_component.get_frequency_type()
        self.frequency_multiplier = seasonality_component.get_frequency_multiplier()
        self.amplitude = seasonality_component.get_amplitude()
        self.phase_shift = seasonality_component.get_phase_shift()

    @abstractmethod
    def calculate(self, dates):
        pass


class DailySeasonalityComponent(Seasonality):
    def calculate(self, dates):
        angular_frequency = 2 * np.pi * self.frequency_multiplier
        return self.amplitude * np.sin(angular_frequency * (dates.hour / 24) + self.phase_shift)


class WeeklySeasonalityComponent(Seasonality):
    def calculate(self, dates):
        angular_frequency = 2 * np.pi * self.frequency_multiplier
        return self.amplitude * np.sin(angular_frequency * (dates.dayofweek / 7) + self.phase_shift)


class MonthlySeasonalityComponent(Seasonality):
    def calculate(self, dates):
        angular_frequency = 2 * np.pi * self.frequency_multiplier
        return self.amplitude * np.sin(angular_frequency * (dates.day / 30) + self.phase_shift)


def calculate_seasonality(dates, series_type, seasonality_component):
    component = np.zeros(len(dates)) if series_type == 'additive' else np.ones(len(dates))
    seasonality=SeasonalityConfigurationManager(seasonality_component)
    frequency_type = seasonality.get_frequency_type()

    if frequency_type == 'daily':
        component += DailySeasonalityComponent(seasonality).calculate(dates)
    elif frequency_type == 'weekly':
        component += WeeklySeasonalityComponent(seasonality).calculate(dates)
    elif frequency_type == 'monthly':
        component += MonthlySeasonalityComponent(seasonality).calculate(dates)
    else:
        raise ValueError("Unsupported frequency_type")

    return pd.Series(component)

from django.core.validators import MinValueValidator
from rest_framework.exceptions import ValidationError
from django.db import models


class Simulator(models.Model):
    """
    Model representing a simulator configuration.

    Attributes:
        name (str): The name of the simulator.
        start_date (DateTime): The start date of the simulation.
        end_date (DateTime): The end date of the simulation.
        series_type (str): The type of time series, either "multiplicative" or "additive".
        producer_type (str): The type of producer, either "kafka" or "CSV" (default is "CSV").
        use_case (str): A description of the simulator's use case.
        meta_data (str): Metadata related to the simulator.
        status (str): The current status of the simulator (e.g., "Submitted", "Running", "Succeeded", "Failed", "Stopped").
        data (JSONField): JSON data associated with the simulator.
        process_id (int): The process ID of the running simulator (nullable).
    """

    SIMULATOR_TYPES = (
        ('multiplicative', 'multiplicative'),
        ('additive', 'additive')
    )

    PRODUCER_TYPE = (
        ('kafka', 'kafka'),
        ('csv', 'CSV')
    )

    SIMULATOR_STATUS = (
        ('Submitted', 'Submitted'),
        ('Running', 'Running'),
        ('Succeeded', 'Succeeded'),
        ('Failed', 'Failed'),
        ('Stopped', 'Stopped')
    )

    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    data_size = models.IntegerField(null=True, validators=[MinValueValidator(1)])
    series_type = models.CharField(max_length=15, choices=SIMULATOR_TYPES)
    producer_type = models.CharField(max_length=10, choices=PRODUCER_TYPE, default='csv')
    use_case = models.CharField(max_length=400)
    meta_data = models.CharField(max_length=400)
    status = models.CharField(max_length=10, choices=SIMULATOR_STATUS, default='Submitted')
    data = models.JSONField(null=True)
    interval = models.IntegerField(null=True)
    process_id = models.IntegerField(null=True)

    # add validation for provide end date or data size
    def save(self, *args, **kwargs):
        # Custom validation logic before saving
        if not self.end_date and not self.data_size:
            raise ValidationError({"end_date": ["Please provide either end date or data size"]})

        super(Simulator, self).save(*args, **kwargs)


class Dataset(models.Model):
    """
    Model representing a dataset configuration.

    Attributes:
        simulator_id (ForeignKey): The foreign key to the associated Simulator.
        cycle_amplitude (int): The cycle amplitude for the dataset (0 for additive, 1 for multiplicative).
        cycle_frequency (float): The cycle frequency of the dataset.
        frequency (str): The frequency of the dataset.
        noise_level (float): The level of noise in the dataset (default is 0).
        trend_coefficient (JSONField): Coefficients for trend components (default is [0, 0, 0]).
        missing_percentage (float): The percentage of missing data (default is 0).
        outlier_percentage (float): The percentage of outliers (default is 0).
        seasonality_components (JSONField): JSON data representing seasonality components (nullable).
    """

    CYCLE_AMPLITUDE_CHOICES = (
        (0, '0 (Additive)'),
        (1, '1 (Multiplicative)'),
    )

    simulator_id = models.ForeignKey(Simulator, on_delete=models.CASCADE)
    cycle_amplitude = models.IntegerField(choices=CYCLE_AMPLITUDE_CHOICES)
    cycle_frequency = models.FloatField()
    frequency = models.CharField(max_length=4)
    noise_level = models.FloatField(default=0)
    trend_coefficient = models.JSONField(default=[0, 0, 0], blank=True, null=True, max_length=3)
    missing_percentage = models.FloatField(default=0)
    outlier_percentage = models.FloatField(default=0)
    seasonality_components = models.JSONField(null=True)


class Seasonality(models.Model):
    """
    Model representing seasonality components for a dataset.

    Attributes:
        dataset_id (ForeignKey): The foreign key to the associated Dataset.
        frequency_type (str): The type of frequency (e.g., "daily", "weekly", "monthly").
        amplitude (float): The amplitude of seasonality component.
        phase_shift (float): The phase shift of seasonality component.
        frequency_multiplier (float): The frequency multiplier of seasonality component.
    """

    FREQUENCY_TYPE = (
        ('daily', 'daily'),
        ('weekly', 'weekly'),
        ('monthly', 'monthly')
    )

    dataset_id = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    frequency_type = models.CharField(choices=FREQUENCY_TYPE, max_length=7, blank=False, null=False)
    amplitude = models.FloatField(default=0)
    phase_shift = models.FloatField(default=0)
    frequency_multiplier = models.FloatField(default=1)

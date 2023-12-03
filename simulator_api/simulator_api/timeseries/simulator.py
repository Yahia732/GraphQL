import logging
import os

from django.db import close_old_connections

from simulator_api import models
from simulator_api.serializers import SimulatorSerializer
from simulator_api.timeseries.generate_time_series import TimeSeries
from simulator_api.timeseries.data_producer import DataProducerCSV
from simulator_api.timeseries.configuration_manager import SimulatorConfigurationManager
import requests
import simplejson
import json


class Simulator:
    def __init__(self, simulator_data):
        simulator_data = json.loads(simulator_data)
        simulator = SimulatorConfigurationManager(simulator_data)
        self.start_date = simulator.get_start_date()
        self.end_date = simulator.get_end_date()
        self.data_size = simulator.get_data_size()
        self.series_type = simulator.get_series_type()
        self.datasets = simulator.get_datasets()
        self.producer_type = simulator.get_producer_type()
        self.file_name = simulator.get_name()

    def generate_data(self):
        """
        Generate the time series data based on seasonality and trend components.

        Returns:
            pandas.DataFrame: The generated time series data.
        """

        for i, dataset in enumerate(self.datasets):
            date_time_series, data, anomaly_mask = TimeSeries(self.start_date, self.end_date, self.series_type,
                                                              self.data_size, dataset).generate_data()
            if self.producer_type == 'csv':
                DataProducerCSV(data=data, date_rng=date_time_series, anomaly=anomaly_mask, file_name=self.file_name,
                                dataset_number=i + 1).save()

            data_list = []
            for i in range(len(date_time_series)):
                date_time_string = date_time_series[i].strftime("%Y-%m-%d %H:%M:%S")
                item = {
                    "date_time_series": date_time_string,
                    "data": data[i],
                    "anomaly_mask": bool(anomaly_mask[i])
                }
                data_list.append(item)





def simulate_simulator(simulator_id):
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproject.settings")
    django.setup()
    """
    Simulate a background process for the specified simulator.

    Args:
        simulator_id: The ID of the simulator to simulate.

    Returns:
        None
    """
    logging.basicConfig(filename=f'simulate_simulator_{simulator_id}.log', level=logging.INFO)
    try:
        logging.info(f'Starting simulation for simulator {simulator_id}')
        close_old_connections()
        # Simulate some background process here
        simulator = models.Simulator.objects.get(id=simulator_id)
        # convert to json
        #close_old_connections()
        simulator_json = json.dumps(SimulatorSerializer(simulator).data)
        Simulator(simulator_json).generate_data()

        logging.info(f'Simulation completed for simulator {simulator_id}')

        # Update the simulator status when the task is completed
        close_old_connections()
        simulator.status = 'Succeeded'
        simulator.save()

    except Exception as e:
        # Update the simulator status when the task is completed
        print(e)
        simulator = models.Simulator.objects.get(id=simulator_id)
        simulator.status = 'Failed'
        simulator.save()
        logging.error(f'Error in simulation for simulator {simulator_id}: {str(e)}')

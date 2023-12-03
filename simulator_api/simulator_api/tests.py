from django.test import TestCase

# Create your tests here.

from django.test import TestCase, Client
from django.urls import reverse
from .models import Simulator
from .serializers import SimulatorSerializer
import json

class SimulatorAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.simulator_data = {
                "name": "Simulator Question",
                "start_date": "1800-09-10T00:00:00Z",
                "end_date": "2023-09-20T00:00:00Z",
                "series_type": "multiplicative",
                "use_case": "Simulator Use Case",
                "meta_data": "Simulator Meta Data",
                "data": [
                    {
                        "cycle_amplitude": 0,
                        "cycle_frequency": 1.0,
                        "frequency": "1D",
                        "noise_level": 0.0,
                        "trend_coefficient": [0, 0, 0],
                        "missing_percentage": 0.05,
                        "outlier_presentation": 0.05,
                        "seasonality_components": [
                            {
                                "frequency_type": "daily",
                                "amplitude": 1.0,
                                "phase_shift": 0.0
                            },
                            {
                                "frequency_type": "weekly",
                                "amplitude": 2.0,
                                "phase_shift": 0.0
                            }
                        ]
                    },
                    {
                        "cycle_amplitude": 1,
                        "cycle_frequency": 2.0,
                        "frequency": "1H",
                        "noise_level": 0.0,
                        "trend_coefficient": [0, 0, 0],
                        "missing_percentage": 0.0,
                        "outlier_presentation": 0.0,
                        "seasonality_components": [
                            {
                                "frequency_type": "daily",
                                "amplitude": 1.0,
                                "phase_shift": 0.0
                            },
                            {
                                "frequency_type": "daily",
                                "amplitude": 2.0,
                                "phase_shift": 0.0
                            }
                        ]
                    }
                ]
            }
        self.simulator = Simulator.objects.create(**self.simulator_data)


    def test_simulator_list_view(self):
        # Test GET request to list simulators
        response = self.client.get(reverse('simulator-list-create'))
        self.assertEqual(response.status_code, 200)

        # assert the response get 1 simulator
        self.assertEqual(len(response.data), 1)

    def test_simulator_create_view(self):
        # Test POST request to create a new simulator
        response = self.client.post(reverse('simulator-list-create'), data=json.dumps(self.simulator_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('simulator-list-create'))
        self.assertEqual(response.status_code, 200)

        # assert the response get 2 simulators
        self.assertEqual(len(response.data), 2)


    def test_run_simulator_view(self):
        # Test POST request to start a simulator
        response = self.client.post(reverse('run-simulator', args=[self.simulator.pk]))
        self.assertEqual(response.status_code, 200)

        # Check if the simulator status is 'Running' after starting
        simulator = Simulator.objects.get(pk=self.simulator.pk)
        self.assertEqual(simulator.status, 'Running')

    def test_stop_simulator_view(self):
        # Start the simulator first
        self.client.post(reverse('run-simulator', args=[self.simulator.pk]))

        # Test POST request to stop the simulator
        response = self.client.post(reverse('stop-simulator', args=[self.simulator.pk]))
        self.assertEqual(response.status_code, 200)

        # Check if the simulator status is 'Stopped' after stopping
        simulator = Simulator.objects.get(pk=self.simulator.pk)
        self.assertEqual(simulator.status, 'Stopped')

    # Add more test cases as needed for other views and scenarios


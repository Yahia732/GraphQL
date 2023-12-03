from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from .models import Simulator, Dataset, Seasonality
from .serializers import SimulatorSerializer, DatasetSerializer, SeasonalitySerializer
from django.views import View
from multiprocessing import Process
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import psutil

from .timeseries.simulator import simulate_simulator


class SimulatorListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating Simulator objects.
    """
    queryset = Simulator.objects.all()
    serializer_class = SimulatorSerializer


class DatasetListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating Dataset objects.
    """
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer


class SeasonalityListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating Seasonality objects.
    """
    queryset = Seasonality.objects.all()
    serializer_class = SeasonalitySerializer


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description='Run a simulator process in the background',
    operation_summary='Run a simulator process in the background',
    responses={
        200: 'Simulator is running in the background.',
        400: 'Simulator is already running.',
    }
))
class RunSimulatorView(View):
    """
    View for starting and running a simulator process in the background.
    """
    def post(self, request, simulator_id):
        """
        Start a simulator process in the background and update its status.

        Args:
            request: The HTTP request object.
            simulator_id: The ID of the simulator to run.

        Returns:
            JsonResponse: JSON response indicating the status of the operation.
        """
        try:
            simulator = Simulator.objects.get(id=simulator_id)
            if simulator.status == 'Running':
                return JsonResponse({'message': f'Simulator {simulator_id} is already running.'})
            # Start the simulator process in the background
            process = Process(target=simulate_simulator, args=(simulator_id,))
            process.start()

            # Update the simulator status when the task is completed and add the process_id
            simulator.process_id = process.pid
            simulator.status = 'Running'
            simulator.save()

            # Respond immediately to the user with a JSON response
            return JsonResponse({'message': f'Simulator {simulator_id} is running in the background.'})
        except Exception as e:
            return JsonResponse({'error': str(e)})



@method_decorator(csrf_exempt, name='dispatch')
class StopSimulatorView(View):
    """
    View for stopping a running simulator process.
    """
    def post(self, request, simulator_id):
        """
        Stop a running simulator process by simulator_id.

        Args:
            request: The HTTP request object.
            simulator_id: The ID of the simulator to stop.

        Returns:
            JsonResponse: JSON response indicating the status of the operation.
        """
        try:
            # Find and terminate the simulator process by simulator_id
            simulator = Simulator.objects.get(id=simulator_id)
            if simulator.status == 'Running':
                psutil.Process(simulator.process_id).terminate()
                simulator.status = 'Stopped'
                simulator.save()
                return JsonResponse({'message': f'Simulator {simulator_id} has been stopped.'})
            else:
                return JsonResponse({'message': f'Simulator {simulator_id} not Running to be stopped.'})
        except Exception as e:
            return JsonResponse({'error': str(e)})

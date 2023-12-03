
from django.urls import path
from .views import SimulatorListCreateView,RunSimulatorView,StopSimulatorView
from graphene_django.views import GraphQLView
from .schema import schema
urlpatterns = [
    path('api/simulators/', SimulatorListCreateView.as_view(), name='simulator-list-create'),
    path('api/run_simulator/<int:simulator_id>', RunSimulatorView.as_view(), name='run-simulator'),
    path('api/stop_simulator/<int:simulator_id>', StopSimulatorView.as_view(), name='stop-simulator'),
    path("graphql",GraphQLView.as_view(graphiql=True,schema=schema))
    #path('api/datasets/',DatasetListCreateView().as_view(), name="dataset-list-creat"),
    #path('api/seasonality/',SeasonalityListCreateView().as_view(), name="dataset-list-creat")
    # Add other API endpoints if needed
]
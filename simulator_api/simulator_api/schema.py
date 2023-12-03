# Import necessary types from graphene
import graphene
from graphene_django.types import DjangoObjectType

from simulator_api.models import Seasonality, Dataset, Simulator


# Define GraphQL types for each Django model
class SimulatorType(DjangoObjectType):
    class Meta:
        model = Simulator

class DatasetType(DjangoObjectType):
    class Meta:
        model = Dataset

class SeasonalityType(DjangoObjectType):
    class Meta:
        model = Seasonality

# Define input types for creating/updating each model
class SimulatorInput(graphene.InputObjectType):
    name = graphene.String()
    start_date = graphene.DateTime()
    end_date = graphene.DateTime()
    data_size = graphene.Int()
    series_type = graphene.String()
    producer_type = graphene.String()
    use_case = graphene.String()
    meta_data = graphene.String()
    status = graphene.String()
    data = graphene.JSONString()
    interval = graphene.Int()
    process_id = graphene.Int()

class DatasetInput(graphene.InputObjectType):
    cycle_amplitude = graphene.Int()
    cycle_frequency = graphene.Float()
    frequency = graphene.String()
    noise_level = graphene.Float()
    trend_coefficient = graphene.JSONString()
    missing_percentage = graphene.Float()
    outlier_percentage = graphene.Float()
    seasonality_components = graphene.JSONString()

class SeasonalityInput(graphene.InputObjectType):
    frequency_type = graphene.String()
    amplitude = graphene.Float()
    phase_shift = graphene.Float()
    frequency_multiplier = graphene.Float()

# Define mutations for creating/updating models
class CreateSimulatorMutation(graphene.Mutation):
    class Arguments:
        input_data = SimulatorInput(required=True)

    simulator = graphene.Field(SimulatorType)

    def mutate(self, info, input_data):
        simulator = Simulator(**input_data)
        simulator.save()
        return CreateSimulatorMutation(simulator=simulator)

class CreateDatasetMutation(graphene.Mutation):
    class Arguments:
        simulator_id = graphene.Int(required=True)
        input_data = DatasetInput(required=True)

    dataset = graphene.Field(DatasetType)

    def mutate(self, info, simulator_id, input_data):
        simulator = Simulator.objects.get(pk=simulator_id)
        dataset = Dataset(simulator_id=simulator, **input_data)
        dataset.save()
        return CreateDatasetMutation(dataset=dataset)

class CreateSeasonalityMutation(graphene.Mutation):
    class Arguments:
        dataset_id = graphene.Int(required=True)
        input_data = SeasonalityInput(required=True)

    seasonality = graphene.Field(SeasonalityType)

    def mutate(self, info, dataset_id, input_data):
        dataset = Dataset.objects.get(pk=dataset_id)
        seasonality = Seasonality(dataset_id=dataset, **input_data)
        seasonality.save()
        return CreateSeasonalityMutation(seasonality=seasonality)



# Define the query root
class Query(graphene.ObjectType):
    simulator = graphene.Field(SimulatorType, id=graphene.Int())
    dataset = graphene.Field(DatasetType, id=graphene.Int())
    seasonality = graphene.Field(SeasonalityType, id=graphene.Int())
    simulators = graphene.List(SimulatorType)
    datasets = graphene.List(DatasetType, simulator_id=graphene.Int())
    simulatorsWithDatasets = graphene.List(SimulatorType)

    def resolve_simulator(self, info, id):
        return Simulator.objects.get(pk=id)

    def resolve_dataset(self, info, id):
        return Dataset.objects.get(pk=id)

    def resolve_seasonality(self, info, id):
        return Seasonality.objects.get(pk=id)

    def resolve_simulators(self, info):
        return Simulator.objects.all()

    def resolve_datasets(self, info, simulator_id):
        return Dataset.objects.filter(simulator_id=simulator_id)

    def resolve_simulatorsWithDatasets(self, info):
        return Simulator.objects.prefetch_related('dataset_set').all()
class UpdateSimulatorStatusMutation(graphene.Mutation):
    class Arguments:
        simulator_id = graphene.Int(required=True)
        new_status = graphene.String(required=True)

    simulator = graphene.Field(SimulatorType)

    def mutate(self, info, simulator_id, new_status):
        simulator = Simulator.objects.get(pk=simulator_id)
        simulator.status = new_status
        simulator.save()
        return UpdateSimulatorStatusMutation(simulator=simulator)

class CreateDatasetWithSeasonalityMutation(graphene.Mutation):
    class Arguments:
        simulator_id = graphene.Int(required=True)
        input_dataset = DatasetInput(required=True)
        input_seasonality = SeasonalityInput(required=True)

    dataset = graphene.Field(DatasetType)

    def mutate(self, info, simulator_id, input_dataset, input_seasonality):
        simulator = Simulator.objects.get(pk=simulator_id)
        dataset = Dataset(simulator_id=simulator, **input_dataset)
        dataset.save()

        seasonality = Seasonality(dataset_id=dataset, **input_seasonality)
        seasonality.save()

        return CreateDatasetWithSeasonalityMutation(dataset=dataset)

# Define the mutation root
class Mutation(graphene.ObjectType):
    create_simulator = CreateSimulatorMutation.Field()
    create_dataset = CreateDatasetMutation.Field()
    create_seasonality = CreateSeasonalityMutation.Field()
    update_simulator_status = UpdateSimulatorStatusMutation.Field()
    create_dataset_with_seasonality = CreateDatasetWithSeasonalityMutation.Field()

# Define the schema
schema = graphene.Schema(query=Query, mutation=Mutation)

from rest_framework import serializers
from .models import Simulator, Dataset, Seasonality

class SeasonalitySerializer(serializers.ModelSerializer):
    """
    Serializer for Seasonality model.

    This serializer is used to serialize and deserialize Seasonality objects.
    """
    class Meta:
        model = Seasonality
        fields = '__all__'


class DatasetSerializer(serializers.ModelSerializer):
    """
    Serializer for Dataset model.

    This serializer is used to serialize and deserialize Dataset objects.
    """
    seasonality = SeasonalitySerializer(many=True, read_only=True)

    class Meta:
        model = Dataset
        fields = '__all__'

    def create(self, validated_data):
        """
        Create a new Dataset instance with related Seasonality components.

        Args:
            validated_data (dict): The validated data for creating the Dataset.

        Returns:
            Dataset: The created Dataset instance.
        """
        seasonality_components = validated_data.pop('seasonality_components')
        dataset = Dataset.objects.create(**validated_data)
        for seasonality_component in seasonality_components:
            # Validate seasonality_component before creating a Seasonality instance
            seasonality_component['dataset_id'] = dataset.id
            seasonality_serializer = SeasonalitySerializer(data=seasonality_component)
            if seasonality_serializer.is_valid():
                seasonality_serializer.save()
            else:
                # If validation fails, raise a ValidationError with the error messages
                raise serializers.ValidationError(seasonality_serializer.errors)
        return dataset

    def to_representation(self, instance):
        """
        Convert the Dataset instance to a serialized representation.

        Args:
            instance (Dataset): The Dataset instance to serialize.

        Returns:
            dict: The serialized representation of the Dataset instance.
        """
        representation = super().to_representation(instance)

        # Include related seasonality components as JSON in the serialized representation
        seasonality_components = Seasonality.objects.filter(dataset_id=instance.id)
        representation['seasonality_components'] = SeasonalitySerializer(seasonality_components, many=True).data
        return representation


class SimulatorSerializer(serializers.ModelSerializer):
    """
    Serializer for Simulator model.

    This serializer is used to serialize and deserialize Simulator objects.
    """
    datasets = DatasetSerializer(many=True, read_only=True)

    class Meta:
        model = Simulator
        fields = '__all__'

    def create(self, validated_data):
        """
        Create a new Simulator instance with related Datasets.

        Args:
            validated_data (dict): The validated data for creating the Simulator.

        Returns:
            Simulator: The created Simulator instance.
        """
        datasets_data = validated_data.pop('data')
        simulator = Simulator.objects.create(**validated_data)

        for dataset_data in datasets_data:
            # Validate dataset_data before creating a Dataset instance
            dataset_data['simulator_id'] = simulator.id
            dataset_serializer = DatasetSerializer(data=dataset_data)
            if dataset_serializer.is_valid():
               dataset_serializer.save()
            else:
                # If validation fails, raise a ValidationError with the error messages
                raise serializers.ValidationError(dataset_serializer.errors)
        return simulator

    def to_representation(self, instance):
        """
        Convert the Simulator instance to a serialized representation.

        Args:
            instance (Simulator): The Simulator instance to serialize.

        Returns:
            dict: The serialized representation of the Simulator instance.
        """
        representation = super().to_representation(instance)

        # Include related datasets as JSON in the serialized representation
        datasets = Dataset.objects.filter(simulator_id=instance.id)
        representation['data'] = DatasetSerializer(datasets, many=True).data

        return representation

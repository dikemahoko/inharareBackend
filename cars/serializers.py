from rest_framework import serializers
from .models import *

# --- Serializers for dropdown data ---
class MakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maker
        fields = ['name']

class ModelNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelName
        fields = ['name']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# --- Serializer for CarType with annotated count ---
class CarTypeSerializer(serializers.ModelSerializer):
    """
    Serializes CarType and includes the annotated car_count from the view.
    """
    car_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CarType
        fields = ['id', 'name', 'image', 'slug', 'car_count']


# --- Serializer for Maker with annotated count ---
class MakerWithCountSerializer(serializers.ModelSerializer):
    """
    Serializes Maker and includes the annotated car_count from the view.
    """
    car_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Maker
        fields = ['id', 'name', 'logo', 'slug', 'car_count']

# --- Main Car Serializer ---
class CarSerializer(serializers.ModelSerializer):
    """
    A comprehensive serializer for Car details.
    Includes nested serializers and source fields for related object names.
    """
    agent_name = serializers.CharField(source='agent.first_name', read_only=True)
    Category_name = serializers.CharField(source='Category.name', read_only=True)
    
    # Nested serializers for richer read-only data
    maker = MakerSerializer(read_only=True)
    model = ModelNameSerializer(read_only=True)
    city = CitySerializer(read_only=True)
    
    class Meta:
        model = Car
        fields = [
            'id', 'title', 'agent', 'agent_name', 'release_date', 'Category', 'Category_name',
            'maker', 'model', 'fuel_type', 'description', 'year', 'price', 
            'mileage', 'transmission', 'color', 'published', 'province', 'city', 
            'is_featured', 'created_at', 'main_image', 'sold'
        ]
        read_only_fields = ['main_image']


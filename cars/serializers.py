from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Car, Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
        
class CarSerializer(serializers.ModelSerializer):
    
    agent_name = serializers.CharField(source='agent.first_name', read_only=True)  # Access the stage_name field
    Category_name = serializers.CharField(source='Category.name', read_only=True)  # Ensure this points to the Category model correctly
   # current_supporters = serializers.IntegerField(source='current_supporters', read_only=True)
    class Meta:
        model = Car
        fields='__all__'


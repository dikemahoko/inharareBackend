from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.db import models
from .serializers import  CarSerializer, CategorySerializer
from .models import Car,  CarActivity, Category

class LatestCarsView(generics.ListAPIView):
    queryset = Car.objects.order_by('-release_date')[:10]
    serializer_class = CarSerializer
    permission_classes = [permissions.AllowAny]

class CarDetailView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]

class AllCarsView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.AllowAny]

    
class AllCategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CarStatisticsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        pass
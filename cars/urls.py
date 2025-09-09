from django.urls import path
from .views import *

urlpatterns = [
    path('cars/', AllCarsView.as_view(), name='all-Cars'),
    path('latest-Cars/', LatestCarsView.as_view(), name='latest-Cars'),
    path('Cars/<int:id>/', CarDetailView.as_view(), name='album-detail'),
    path('Cars/<int:id>/statistics/', CarStatisticsView.as_view(), name='album-statistics'),
    path('Cars/category',AllCategoryView.as_view(),name='categoryview')
]

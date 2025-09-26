from django.urls import path
from .views import *

urlpatterns = [
    # Public car browsing endpoints
    path('cars/', AllCarsView.as_view(), name='all-cars'),
    path('cars/latest/', LatestCarsView.as_view(), name='latest-cars'),
    path('cars/<int:id>/', CarDetailView.as_view(), name='car-detail'),
    path('cars/<int:id>/statistics/', CarStatisticsView.as_view(), name='car-statistics'),

    # Dropdown data endpoints
    path('categories/', AllCategoryView.as_view(), name='all-categories'),
    path('makers/', AllMakersView.as_view(), name='all-makers'),
    path('models/', AllModelsView.as_view(), name='all-models'),
    path('cities/', AllCitiesView.as_view(), name='all-cities'),

    # User action endpoints (liking, enquiring, etc.)
    path('cars/<int:id>/like/', CarLikeView.as_view(), name='car-like'),
    path('cars/<int:id>/enquire/', CarEnquiryView.as_view(), name='car-enquire'),
    path('cars/<int:id>/sold/', CarMarkSoldView.as_view(), name='car-mark-sold'),
    path('cars/featured/', FeaturedCarsView.as_view(), name='featured-cars'),

    # Endpoints for users to manage their own listings
    path('my-cars/', UserCarsView.as_view(), name='user-cars-list'),
    path('my-cars/<int:id>/', UserCarDetailView.as_view(), name='user-car-detail'),
    path('body-types/', CarTypeWithCountView.as_view(), name='body-types'),
    path('makers/with-count/', MakerWithCountView.as_view(), name='makers-with-count'),
]


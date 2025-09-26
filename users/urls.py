from django.urls import path, re_path
from .views import (
    CustomProviderAuthView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    LogoutView,UserAccountUpdateView,
    UserAccountUpdateView,
    FeaturedDealersView
)

urlpatterns = [
    re_path(
        r'^o/(?P<provider>\S+)/$',
        CustomProviderAuthView.as_view(),
        name='provider-auth'
    ),
   # path('profile/edit/', UserAccountUpdateView.as_view(), name='edit-profile'),
    path('update-profile/', UserAccountUpdateView.as_view(), name='update-profile'),
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView.as_view()),
      path('dealers/featured/', FeaturedDealersView.as_view(), name='featured-dealers'),
]


# # Djoser URLs
#     path('auth/', include('djoser.urls')),
#     path('auth/', include('djoser.urls.jwt')),
    
#     # Custom social auth URL
#     path('auth/o/google-oauth2/', CustomGoogleAuthView.as_view(), name='google-auth'),
    
#     # Keep the general provider URL for other providers
#     path('auth/o/<str:provider>/', CustomGoogleAuthView.as_view(), name='provider-auth')
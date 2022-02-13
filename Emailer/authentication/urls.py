from django.urls import path
from rest_framework_simplejwt import views

urlpatterns = [
    path("refresh", views.TokenObtainPairView.as_view()),
    path("", views.TokenRefreshView.as_view()),
]

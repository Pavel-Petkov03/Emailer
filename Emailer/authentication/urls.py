from django.urls import path
from rest_framework_simplejwt import views
from .views import RegisterAPIView




urlpatterns = [
    path("login", views.TokenObtainPairView.as_view()),
    path("refresh", views.TokenRefreshView.as_view()),
    path("register", RegisterAPIView.as_view()),
]

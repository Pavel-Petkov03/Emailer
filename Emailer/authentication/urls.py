from django.urls import path
from rest_framework_simplejwt import views

from Emailer.authentication.views import  RegisterAPIView

urlpatterns = [
    path("refresh", views.TokenObtainPairView.as_view()),
    path("", views.TokenRefreshView.as_view()),
    path("register", RegisterAPIView.as_view()),
]

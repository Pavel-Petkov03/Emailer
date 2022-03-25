from django.urls import path
from Emailer.authentication.views import LoginView, RegisterView
urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
]

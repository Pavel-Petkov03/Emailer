from django.shortcuts import render
from django.urls import path

from Emailer.authentication.views import LoginView, RegisterView
from Emailer.main.views import EmailDetailView


def test(req):
    return render(req, "folder.html")


urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path("table", test),
    path("table/<int:pk>", EmailDetailView.as_view())
]

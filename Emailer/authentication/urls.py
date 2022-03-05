from django.shortcuts import render
from django.urls import path

from Emailer.authentication.views import LoginView, RegisterView


def test(req):
    return render(req, "table.html")


def l(req):


    print(12)
    print(12342341)
    return render(req, "add_receiver.html")


urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path("table", test),
    path("add-receiver", l)
]

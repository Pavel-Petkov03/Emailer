from django.shortcuts import render
from django.urls import path

from Emailer.main.views import ReceiverView, GroupView


def send(req):
    return render(req, "send_email.html")


urlpatterns = [
    path("add-receiver", ReceiverView.as_view(), name="add receiver"),
    path("add-group", GroupView.as_view(), name="add group"),
    path("send", send)
]

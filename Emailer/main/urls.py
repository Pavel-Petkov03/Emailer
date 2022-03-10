from django.shortcuts import render
from django.urls import path

from Emailer.main.views import ReceiverView, GroupView, SendEmailView




urlpatterns = [
    path("add-receiver", ReceiverView.as_view(), name="add receiver"),
    path("add-group", GroupView.as_view(), name="add group"),
    path("send", SendEmailView.as_view())
]

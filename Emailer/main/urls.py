from django.shortcuts import render
from django.urls import path

from Emailer.main.views import ReceiverView, GroupView,  EmailDetailView, SendSingleEmailView, SendMassEmailView


def folder(req):
    return render(req, "folder.html")


def _bin(req):
    return render(req, "bin.html")


urlpatterns = [
    path("folder/<int:pk>", EmailDetailView.as_view()),
    path("folder", folder, name="folder"),
    path("bin/<int:pk>", EmailDetailView.as_view()),
    path("bin", _bin, name="bin"),
    path("add-receiver", ReceiverView.as_view(), name="add receiver"),
    path("add-group", GroupView.as_view(), name="add group"),
    path("send", SendSingleEmailView.as_view()),
    path("group/send/<int:pk>", SendMassEmailView.as_view(), name="preview group")
]

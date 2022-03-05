from django.urls import path

from Emailer.main.views import ReceiverView, GroupView

urlpatterns = [
    path("add-receiver", ReceiverView.as_view(), name="add receiver"),
    path("add-group", GroupView.as_view(), name="add group")
]

from django.urls import path

from Emailer.main.views import ReceiverView

urlpatterns = [
    path("add-receiver", ReceiverView.as_view(), name="add receiver")
]

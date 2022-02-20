from django.urls import path

from Emailer.main.views import SendEmailView

urlpatterns = [
    path("send", SendEmailView.as_view())
]

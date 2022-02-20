from django.urls import path

from Emailer.main.views import SendEmailView, CreateCustomTemplate

urlpatterns = [
    path("send", SendEmailView.as_view()),
    path("create_template", CreateCustomTemplate.as_view())
]

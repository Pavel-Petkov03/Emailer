from django.urls import path

from Emailer.main.views import EmailView, CustomTemplateView

urlpatterns = [
    path("send", EmailView.as_view()),
    path("create_template", CustomTemplateView.as_view())
]

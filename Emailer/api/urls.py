from django.urls import path

from Emailer.api.views import GroupView

urlpatterns = [
    path("group", GroupView.as_view())
]

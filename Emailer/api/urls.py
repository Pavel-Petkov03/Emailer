from django.urls import path

from Emailer.api.views import GroupView, Folder

urlpatterns = [
    path("group", Folder.as_view())
]

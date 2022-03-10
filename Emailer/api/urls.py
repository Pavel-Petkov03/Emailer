from django.urls import path

from Emailer.api.views import GroupView, Folder

urlpatterns = [
    path("folder", Folder.as_view(), name="folder")
]

from django.urls import path

from Emailer.api.views import GroupView, Folder, FilterEmail

urlpatterns = [
    path("folder", Folder.as_view(), name="folder"),
    path("filter", FilterEmail.as_view())
]

from django.urls import path

from Emailer.api.views import GenericFolder, FilterEmail

urlpatterns = [
    path("folder", GenericFolder.as_view()),
    path("filter", FilterEmail.as_view())
]

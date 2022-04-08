from django.urls import path
from Emailer.api.views import GenericFolder, FilterEmail, DeleteEmailView, DeleteReceiverView

urlpatterns = [
    path("folder", GenericFolder.as_view()),
    path("filter", FilterEmail.as_view()),
    path("email/<int:pk>", DeleteEmailView.as_view()),
    path("receiver/<int:pk>", DeleteReceiverView.as_view())
]

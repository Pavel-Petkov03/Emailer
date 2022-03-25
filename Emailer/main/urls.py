
from django.urls import path
from Emailer.main.views.email_views import EmailDetailView, SendSingleEmailView, SendMassEmailView, Folder, Bin
from Emailer.main.views.many_to_many_views import ReceiverView, GroupView
urlpatterns = [
    path("folder/<int:pk>", EmailDetailView.as_view()),
    path("folder", Folder.as_view(), name="folder"),
    path("bin/<int:pk>", EmailDetailView.as_view()),
    path("bin", Bin.as_view(), name="bin"),
    path("add-receiver", ReceiverView.as_view(), name="add receiver"),
    path("add-group", GroupView.as_view(), name="add group"),
    path("send", SendSingleEmailView.as_view()),
    path("group/send/<int:pk>", SendMassEmailView.as_view(), name="preview group")
]

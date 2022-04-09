from django.urls import path
from Emailer.authentication.views import LoginView, RegisterView, EditProfileView, LogoutView

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path("edit-profile", EditProfileView.as_view(), name="edit-profile"),
    path("logout", LogoutView.as_view(), name="logout")
]
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from Emailer.authentication.forms import LoginForm, RegisterForm, EditProfileForm
from django.contrib.auth import views

class LoginView(views.LoginView):
    form_class = LoginForm

class RegisterView(View):
    template = "registration/register.html"
    redirect_success = "/"
    form = RegisterForm

    def get(self, req):
        return render(req, self.template, {
            "form": self.form()
        })

    def post(self, req):
        form = self.form(req.POST)
        if form.is_valid():
            form.save()
            return redirect(self.redirect_success)
        return render(req, self.template, {
            "form": form
        })


class EditProfileView(View):
    form = EditProfileForm

    def get(self, request):
        return render(request, "edit_profile.html", {"form": self.form()})

    def post(self, request):
        form = self.form(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("add group")
        return render(request, "edit_profile.html", {"form": form})

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from Emailer.authentication.forms import LoginForm, RegisterForm


class LoginView(View):
    template = "registration/login.html"

    def get(self, req):
        return render(req, self.template, {
            "form": LoginForm()
        })

    def post(self, req):
        print(req.POST)
        form = LoginForm(req.POST)
        if form.is_valid():
            user = form.login()
            if user:
                login(req, user)
                return redirect("folder")
        return render(req, self.template, {
            "form": form
        })


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



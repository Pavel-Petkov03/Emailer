from django.shortcuts import render, redirect
from django.views import View

from Emailer.main.forms import LoginForm, RegisterForm


class CustomAuthView(View):
    form = None
    template = None
    redirect_success = None

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


class LoginView(CustomAuthView):
    template = "login.html"
    redirect_success = ""
    form = LoginForm


class RegisterView(CustomAuthView):
    template = "register.js"
    redirect_success = ""
    form = RegisterForm

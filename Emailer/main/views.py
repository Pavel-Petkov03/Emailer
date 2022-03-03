from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail

from Emailer.main.forms import LoginForm, RegisterForm


class LoginView(View):
    template = "registration/login.html"

    def get(self, req):
        return render(req, self.template, {
            "form": LoginForm()
        })

    def post(self, req):
        form = LoginForm(req.POST)
        if form.is_valid():
            user = form.login()
            if user:
                login(req, user)
                return redirect("/")
        return render(req, self.template, {
            "form": form
        })


class RegisterView(View):
    template = "register.html"
    redirect_success = "/"
    form = RegisterForm

    def get(self, req):
        return render(req, self.template, {
            "form": self.form()
        })

    def post(self, req):
        form = self.form(req.POST)
        if form.is_valid():
            form.save(req)
            return redirect(self.redirect_success)
        return render(req, self.template, {
            "form": form
        })


class SendEmail:
    model = None

    def send_singular_mail(self, *args, **kwargs):
        send_mail(*args, **kwargs)

    def send_many_mails(self):
        pass

    def authenticate_mail(self, user):
        if user.email_password is not None:
            pass

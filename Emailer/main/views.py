from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail

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
    template = "register.html"
    redirect_success = ""
    form = RegisterForm


class SendEmail:
    model = None

    def send_singular_mail(self, *args, **kwargs):
        send_mail(*args, **kwargs)

    def send_many_mails(self):
        pass

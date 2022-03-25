from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from Emailer.main.forms.email_forms import SendMassEmailForm, SendSingleEmailForm
from Emailer.main.models import Group, Email
from Emailer.main.views.base_views import BaseEmailView


class SendSingleEmailView(BaseEmailView):
    form_class = SendSingleEmailForm
    template = "send-single-email.html"
    success_redirect = "folder"


class SendMassEmailView(BaseEmailView):
    form_class = SendMassEmailForm
    template = "send_mass_email.html"
    success_redirect = "folder"

    @staticmethod
    def additional_get_kwargs(req, pk):
        group = Group.objects.get(id=pk)
        query = group.receivers.all()
        return {
            "receivers": query,
            "group_name": group.name
        }


@method_decorator(login_required(login_url="login"), name="dispatch")
class EmailDetailView(View):
    def get(self, req, pk):
        current_email = Email.objects.get(receiver__user=req.user, id=pk)
        return render(req, "email-description.html", {
            "image": current_email.screenshot
        })


@method_decorator(login_required(login_url="login"), name="dispatch")
class Folder(View):
    def get(self, req):
        return render(req, "folder.html")

@method_decorator(login_required(login_url="login"), name="dispatch")
class Bin(View):
    def get(self, req):
        return render(req, "bin.html")

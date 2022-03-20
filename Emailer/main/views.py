from abc import ABC, abstractmethod
from smtplib import SMTPAuthenticationError

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from Emailer.authentication.views import LoginRequiredView
from Emailer.main.models import Preferences, Receiver, Email, Group
from Emailer.main.forms import ReceiverForm, GroupForm, SendEmailForm, FilterForm


class ManyToManyModelCustomView(LoginRequiredView, ABC):
    """
    this class works only if you put Model form and if you have many to many relationship
    """
    form_class = None
    template = None
    many_to_many_argument = None
    success_url = None

    def get(self, req):
        form = self.form_class()
        return render(req, self.template, {
            "form": form
        })

    def post(self, req):
        post_data = req.POST.copy()
        post_data.setlist(self.many_to_many_argument,
                          self.convert_from_many_to_many_arg_to_id(post_data.getlist(self.many_to_many_argument)))
        form = self.form_class(post_data)
        if form.is_valid():
            custom_model_field = form.save(commit=False)
            custom_model_field.user = req.user
            custom_model_field.save()
            form.save_m2m()
            return redirect(self.success_url)

        return render(req, self.template, {
            "form": form
        })

    @abstractmethod
    def convert_from_many_to_many_arg_to_id(self, array_of_fields):
        """

        :return: array with id's which will be saved via save_m2m()
        this function must be overridden
        """
        return True


class ReceiverView(ManyToManyModelCustomView):
    form_class = ReceiverForm
    template = "add_receiver.html"
    many_to_many_argument = "preferences"
    success_url = "login"

    def convert_from_many_to_many_arg_to_id(self, array_of_fields):
        return [str(preference.id) for preference in Preferences.objects.filter(hobby__in=array_of_fields)]


class GroupView(ManyToManyModelCustomView):
    form_class = GroupForm
    template = "add_group.html"
    many_to_many_argument = "receivers"
    success_url = "login"

    def get(self, req):
        form = self.form_class()
        filter_form = FilterForm()
        return render(req, self.template, {
            "form": form,
            "filter_form": filter_form
        })

    def convert_from_many_to_many_arg_to_id(self, array_of_fields):
        return [str(receiver.id) for receiver in Receiver.objects.filter(email__in=array_of_fields)]


class SendEmailView(LoginRequiredView):

    def get(self, req):
        form = SendEmailForm()
        return render(req, "send_email.html", {
            "form": form
        })

    def post(self, req):
        form = SendEmailForm(req.POST)
        if form.is_valid():
            try:
                form.save(req.user)
            except SMTPAuthenticationError:
                form.add_error(None, ValidationError("The email and the password of your email must match"))
                return render(req, "send_email.html", {
                    "form": form
                })
            return redirect("add receiver")
        return render(req, "send_email.html", {
            "form": form,
        })


class EmailDetailView(LoginRequiredView):
    def get(self, req, pk):
        current_email = Email.objects.get(receiver__user=req.user, id=pk)
        return render(req, "email-description.html", {
            "image": current_email.screenshot
        })

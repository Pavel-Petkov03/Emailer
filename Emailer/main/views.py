from abc import ABC, abstractmethod
from smtplib import SMTPAuthenticationError

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from Emailer.authentication.views import LoginRequiredView
from Emailer.main.models import Preferences, Receiver, Email, Group
from Emailer.main.forms import ReceiverForm, GroupForm, FilterForm, SendSingleEmailForm, SendMassEmailForm


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


class GenericEmailView(LoginRequiredView):
    """
    This class will be based of email sending class
    In this class will be bing a sending from which inherits GenericSendEmailForm

    """
    form_class = None
    template = None
    success_redirect = None

    def get(self, req, pk=None):
        form = self.form_class()
        return render(req, self.template, {
            "form": form,
            **self.additional_get_kwargs(req, pk)
        })

    def post(self, req, pk=None):
        form = self.form_class(req.POST)
        if form.is_valid():
            try:
                form.save(req.user, pk)
            except SMTPAuthenticationError:
                form.add_error(None, ValidationError("The email and the password of your email must match"))
                return render(req, self.template, {
                    "form": form,
                })
            success_redirect = self.success_redirect
            return redirect(success_redirect)
        return render(req, self.template, {
            "form": form,
        })

    @staticmethod
    def additional_get_kwargs(req, pk):

        """
        This function will be overridden if need to pass additional args to get
        :return: {}
        """
        return {}


class SendSingleEmailView(GenericEmailView):
    form_class = SendSingleEmailForm
    template = "send-single-email.html"
    success_redirect = "folder"


class SendMassEmailView(GenericEmailView):
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


class EmailDetailView(LoginRequiredView):
    def get(self, req, pk):
        current_email = Email.objects.get(receiver__user=req.user, id=pk)
        return render(req, "email-description.html", {
            "image": current_email.screenshot
        })

from abc import ABC, abstractmethod
from django.shortcuts import render, redirect

from Emailer.authentication.views import LoginRequiredView
from Emailer.main.models import Preferences, Receiver
from Emailer.main.forms import ReceiverForm, GroupForm, SendEmailForm
from html2image import Html2Image

from Emailer.main.utils import Sender


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

    def convert_from_many_to_many_arg_to_id(self, array_of_fields):
        return [str(receiver.id) for receiver in Receiver.objects.filter(mail__in=array_of_fields)]


# class Ra:
#     htm = Html2Image(output_path="")
#     htm.screenshot(html_file="", save_as="", )


class SendEmailView(LoginRequiredView):

    def get(self, req):
        form = SendEmailForm()
        return render(req, "send_email.html", {
            "form": form
        })

    def post(self, req):
        form = SendEmailForm(req.POST)
        if form.is_valid():
            form.save(req.user)
            return redirect("add receiver")
        return render(req, "send_email.html", {
            "form": form
        })

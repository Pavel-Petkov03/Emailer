from abc import ABC, abstractmethod
from smtplib import SMTPAuthenticationError

from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from Emailer.authentication.views import LoginRequiredView


class BaseManyToManyView(LoginRequiredView, ABC):
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
        form = self.form_class(post_data, user=req.user)
        if form.is_valid():
            form.save(commit=True)
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


class BaseEmailView(LoginRequiredView):
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
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from Emailer.main.models import Receiver


class Sender:
    __instance = None
    """
    This class will send mails and mass mails
    There won't be two instances of this class
    """

    def __init__(self):
        if Sender.__instance is None:
            Sender.__instance = self
        else:
            raise Exception("This class must not be instanced")

    @staticmethod
    def get_instance():
        if Sender.__instance is None:
            Sender()
        return Sender.__instance

    def send_single_mail(self, subject, message, sender, receiver: Receiver, template):
        (html_message, plain_message) = self.__get_raw_message(sender, message, template)
        send_mail(subject, plain_message, sender.auth_mail, [receiver.mail], auth_user=sender.auth_mail,
                  auth_password=sender.auth_password, html_message=html_message)

    def send_mass_mail(self, subject, message, sender, query: [Receiver]):
        pass



    @staticmethod
    def _get_context(user, message):
        variable_names = ["first_name", "last_name", "age"]
        user_kwargs = {arg: user[arg] for arg in variable_names if user[arg] is not None}
        user_kwargs[message] = message
        return user_kwargs

    def __get_raw_message(self, user, message, template):
        context = self._get_context(user, message)
        html_message = render_to_string(template, context=context)
        plain_message = strip_tags(html_message)
        return (html_message, plain_message)

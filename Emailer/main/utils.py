from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from Emailer.main.models import Receiver


class Sender:
    instance = None
    """
    This class will send mails and mass mails
    There won't be two instances of this class
    """

    def __init__(self):
        if Sender.instance is None:
            Sender.instance = self
        else:
            raise Exception("This class must not be instanced")

    @staticmethod
    def get_instance():
        if Sender.instance is None:
            Sender()
        return Sender.instance

    def send_single_mail(self, subject, message, sender, receiver: Receiver, template) -> None:
        (html_message, plain_message) = self.__get_raw_message(receiver, message, template)
        send_mail(subject, plain_message, sender.auth_mail, [receiver.mail], auth_user=sender.auth_mail,
                  auth_password=sender.auth_password, html_message=html_message, fail_silently=False)

    def send_mass_mail(self, subject: str, message: str, sender: AbstractUser, receivers: [Receiver], template) -> None:
        send_mass_mail(self.populate_data_tuple(subject, message, sender, receivers, template),
                       auth_user=sender.auth_mail,
                       auth_password=sender.auth_password, fail_silently=False)

    def populate_data_tuple(self, subject: str, message: str, sender: AbstractUser, receivers: [Receiver],
                            template: str):
        recipients = self.get_all_recipients_mails(receivers)
        return (self.populate_one_entry(subject, message, sender, receiver, template, recipients) for receiver in
                receivers)

    def populate_one_entry(self, subject, message, sender, receiver, template, recipient_list):
        (html_message, plain_message) = self.__get_raw_message(receiver, message, template)
        return subject, plain_message, sender.auth_mail, recipient_list

    @staticmethod
    def get_all_recipients_mails(receivers) -> list:
        return [receiver.mail for receiver in receivers]

    @staticmethod
    def _get_context(user, message) -> dict:
        variable_names = ["first_name", "last_name", "age"]
        user_kwargs = {arg: user[arg] for arg in variable_names if user[arg] is not None}
        user_kwargs[message] = message
        return user_kwargs

    def __get_raw_message(self, receiver: Receiver, message, template) -> tuple:
        context = self._get_context(receiver, message)
        html_message = render_to_string(template, context=context)
        plain_message = strip_tags(html_message)
        return html_message, plain_message

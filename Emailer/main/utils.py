from django.core.mail import send_mail, send_mass_mail
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from typing import Union
from Emailer.authentication.models import CustomUserModel
from Emailer.main.models import Receiver


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Sender(metaclass=SingletonMeta):
    """
    This class will send mails and mass mails
    There won't be two instances of this class
    """

    def send_single_mail(self, subject: str, message: str, sender: CustomUserModel, receiver: Receiver,
                         template: str) -> None:
        (html_message, plain_message) = self.__get_raw_message(receiver, message, template)
        send_mail(subject, plain_message, sender.email, [receiver.email], auth_user=sender.email,
                  auth_password=sender.password, html_message=html_message, fail_silently=False)

    def send_mass_mail(self, subject: str, message: str, sender: CustomUserModel, receivers: [Receiver],
                       template) -> None:
        send_mass_mail(self.__populate_data_tuple(subject, message, sender, receivers, template),
                       auth_user=sender.email,
                       auth_password=sender.password, fail_silently=False)

    def __populate_data_tuple(self, subject: str, message: str, sender: CustomUserModel,
                              receivers: Union[QuerySet, list[Receiver]],
                              template: str):
        recipients = self.__get_all_recipients_mails(receivers)
        return (self.__populate_one_entry(subject, message, sender, receiver, template, recipients) for receiver in
                receivers)

    def __populate_one_entry(self, subject: str, message: str, sender: CustomUserModel, receiver: Receiver,
                             template: str,
                             recipient_list: list[Receiver]):
        (html_message, plain_message) = self.__get_raw_message(receiver, message, template)
        return subject, plain_message, sender.email, recipient_list

    @staticmethod
    def __get_all_recipients_mails(receivers) -> list:
        return [receiver.mail for receiver in receivers]

    @staticmethod
    def __get_context(user: Receiver, message) -> dict:
        variable_names = ["first_name", "last_name", "age"]
        user_kwargs = {arg: getattr(user, arg) for arg in variable_names if getattr(user, arg) is not None}
        user_kwargs[message] = message
        return user_kwargs

    def __get_raw_message(self, receiver: Receiver, message, template) -> tuple:
        context = self.__get_context(receiver, message)
        html_message = render_to_string(template, context=context)
        plain_message = strip_tags(html_message)
        return html_message, plain_message

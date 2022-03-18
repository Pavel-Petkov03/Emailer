from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from html2image import Html2Image

from Emailer.authentication.models import CustomUserModel
from Emailer.main.models import Receiver, Email


class Sender:
    """
    This class will send mails and mass mails
    """

    def __init__(self, subject: str, message: str, sender: CustomUserModel, receivers: [Receiver], template: str):
        self.subject = subject
        self.message = message
        self.sender = sender
        self.receivers = receivers
        self.template = template

    def send_single_mail(self) -> str:
        (html_message, plain_message) = self.__get_raw_message(self.receivers[0])
        send_mail(self.subject, plain_message, self.sender.email, [self.receivers[0].email],
                  auth_user=self.sender.email,
                  auth_password=self.sender.email_password, html_message=html_message, fail_silently=False)

        return html_message

    def send_mass_mail(self) -> None:
        send_mass_mail(self.__populate_data_tuple(),
                       auth_user=self.sender.email,
                       auth_password=self.sender.email_password, fail_silently=False)

    def __populate_data_tuple(self):
        return (self.__populate_one_entry(receiver) for receiver in
                self.receivers)

    def __populate_one_entry(self, receiver: Receiver):
        recipients = self.__get_all_recipients_mails(self.receivers)
        (html_message, plain_message) = self.__get_raw_message(receiver)
        return self.subject, plain_message, self.sender.email, recipients

    @staticmethod
    def __get_all_recipients_mails(receivers) -> list:
        return [receiver.mail for receiver in receivers]

    def __get_context(self, user: Receiver) -> dict:
        variable_names = ["first_name", "last_name", "age"]
        user_kwargs = {arg: getattr(user, arg) for arg in variable_names if getattr(user, arg) is not None}
        user_kwargs["message"] = self.message
        return user_kwargs

    def __get_raw_message(self, receiver: Receiver) -> tuple:
        context = self.__get_context(receiver)
        html_message = render_to_string(self.template, context=context)
        plain_message = strip_tags(html_message)
        return html_message, plain_message


class EmailDispatcher(Sender):
    def send_single_mail(self) -> None:
        html_str = super().send_single_mail()
        saver = Html2Image(output_path=settings.BASE_DIR / "media")
        screenshot_path = saver.screenshot(html_str=html_str)[0]
        email = Email(subject=self.subject, receiver=self.receivers[0], date=datetime.now(), screenshot=screenshot_path)
        email.save()

    def send_mass_mail(self) -> None:
        super().send_mass_mail()

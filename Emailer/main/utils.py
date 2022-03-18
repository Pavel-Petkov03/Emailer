import os.path
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from html2image import Html2Image
from Emailer.main.models import Receiver, Email



class Sender:
    """
    This class will send emails and mass emails
    """

    def __init__(self, subject=None, message=None, sender=None, receivers=None, template=None):
        self.subject = subject
        self.message = message
        self.sender = sender
        self.receivers = receivers
        self.template = template
        self.recipients = self.__get_all_recipients_mails(receivers)

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, value):
        if not isinstance(value, str):
            raise ValueError("subject must be string")
        self.__subject = value

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if not isinstance(value, str):
            raise ValueError("message must be string")
        self.__message = value

    @property
    def receivers(self):
        return self.__receivers

    @receivers.setter
    def receivers(self, value):
        if not isinstance(value, list) or not all([receiver for receiver in value if isinstance(receiver, Receiver)]):
            raise ValueError("receivers must be a list of receivers")
        self.__receivers = value

    @property
    def template(self):
        return self.__template

    @template.setter
    def template(self, value):
        if not isinstance(value, str):
            raise ValueError("template must be string path")
        if not os.path.exists(value):
            raise ValueError("template path must exist")
        self.__template = value

    def send_single_mail(self) -> str:
        (html_message, plain_message) = self.__get_raw_message(self.receivers[0])
        send_mail(self.subject, plain_message, self.sender.email, [self.receivers[0].email],
                  auth_user=self.sender.email,
                  auth_password=self.sender.email_password, html_message=html_message, fail_silently=False)

        return html_message

    def send_mass_mail(self):
        data_tuple = self.__populate_data_tuple()
        send_mass_mail(data_tuple,
                       auth_user=self.sender.email,
                       auth_password=self.sender.email_password, fail_silently=False)
        return data_tuple

    def __populate_data_tuple(self):
        return (self.__populate_one_entry(receiver) for receiver in
                self.receivers)

    def __populate_one_entry(self, receiver: Receiver):
        (html_message, plain_message) = self.__get_raw_message(receiver)
        return self.subject, plain_message, self.sender.email, self.recipients

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
    """
    This class inherits mail sending and if acquires success makes instances in db
    """

    def send_single_mail(self) -> None:
        html_str = super().send_single_mail()
        screenshot_path = self.create_screenshot(html_str)
        email_instance = self.create_email_instance(screenshot_path, self.receivers[0])
        email_instance.save()

    def send_mass_mail(self) -> None:
        data_tuple = super().send_mass_mail()
        email_list = []
        for index, entry in enumerate(data_tuple):
            html_str = entry[1]
            receiver = self.receivers[index]
            screenshot_path = self.create_screenshot(html_str)
            email_list.append(self.create_email_instance(screenshot_path, receiver))
        Email.objects.bulk_create(email_list)

    @staticmethod
    def create_screenshot(html_str):
        saver = Html2Image(output_path=settings.BASE_DIR / "media")
        screenshot_path = saver.screenshot(html_str=html_str)[0]
        return screenshot_path

    def create_email_instance(self, screenshot_path, receiver: Receiver):
        return Email(subject=self.subject, receiver=receiver, date=datetime.now(), screenshot=screenshot_path)

    @staticmethod
    def retrieve_html_strings(data_tuple):
        """
        :param data_tuple:
        :return: list[html_str]
        """
        return [entry[1] for entry in data_tuple]

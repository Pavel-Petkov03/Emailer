import random
import string
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from html2image import Html2Image
from Emailer.main.models import Receiver, Email
from cloudinary.uploader import upload
import shutil


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
        # if not isinstance(value, list) or not all([receiver for receiver in value if isinstance(receiver, Receiver)]):
        #     raise ValueError("receivers must be a list of receivers")
        self.__receivers = value

    def send_single_mail(self) -> str:
        (html_message, plain_message) = self.__get_raw_message(self.receivers[0])
        send_mail(self.subject, plain_message, self.sender.email, self.recipients,
                  auth_user=self.sender.email,
                  auth_password=self.sender.email_password, html_message=html_message, fail_silently=False)

        return html_message

    def send_mass_mail(self):
        connection = get_connection(
            username=self.sender.email, password=self.sender.email_password, fail_silently=False)
        message_list = []
        html_messages = []
        for receiver in self.receivers:
            *message_props, html_message = self.__populate_one_entry(receiver)
            html_messages.append(html_message)
            message = EmailMultiAlternatives(*message_props)
            message.attach_alternative(html_message, "text/html")
            message_list.append(message)
        connection.send_messages(message_list)
        return html_messages

    def __populate_one_entry(self, receiver: Receiver):
        (html_message, plain_message) = self.__get_raw_message(receiver)
        return self.subject, plain_message, self.sender.email, self.recipients, html_message

    @staticmethod
    def __get_all_recipients_mails(receivers) -> list:
        return [receiver.email for receiver in receivers]

    def __get_context(self, user: Receiver) -> dict:
        variable_names = ["first_name", "last_name", "age"]
        user_kwargs = {arg: getattr(user, arg) for arg in variable_names if getattr(user, arg) is not None}
        user_kwargs["message"] = self.message
        return user_kwargs

    def __get_raw_message(self, receiver: Receiver) -> tuple:
        context = self.__get_context(receiver)
        html_message = render_to_string(self.template.template.path, context=context)
        plain_message = strip_tags(html_message)
        return html_message, plain_message


class EmailDispatcher(Sender):
    """
    This class inherits mail sending and if acquires success makes instances in db
    """

    def send_single_mail(self) -> None:
        html_str = super().send_single_mail()
        screenshot_path = self.create_screenshot([html_str], self.__generate_file_location())[0]
        email_instance = self.create_email_instance(screenshot_path, self.receivers[0])
        email_instance.save()
        self.clean_paths()

    def send_mass_mail(self) -> None:
        data_tuple = super().send_mass_mail()
        html_strings = [entry for entry in data_tuple]
        file_locations = self.__generate_file_location()
        path_list = self.create_screenshot(html_strings, file_locations)
        email_list = [self.create_email_instance(path_list[index], entry) for index, entry in enumerate(self.receivers)]
        Email.objects.bulk_create(email_list)
        self.clean_paths()

    @staticmethod
    def create_screenshot(html_strings: list, file_locations: list):
        saver = Html2Image(output_path=settings.BASE_DIR / "media/screenshots", )
        screenshot_path = saver.screenshot(html_str=html_strings, save_as=file_locations)
        return screenshot_path

    def create_email_instance(self, screenshot_path, receiver: Receiver):
        image = self.save_image(screenshot_path)
        instance = Email(subject=self.subject, receiver=receiver,
                         screenshot=image["url"],
                         template=self.template)
        return instance

    @staticmethod
    def save_image(path):
        with open(path, "rb") as file:
            value = upload(file, folder="Emailer")
        return value

    def __generate_file_location(self):
        file_location_list = []
        for receiver in self.receivers:
            receiver_id = receiver.id
            sender_id = receiver.user.id
            location = f'{sender_id}-{receiver_id}-{self.__generate_random_id()}' + ".png"
            file_location_list.append(location)
        return file_location_list

    @staticmethod
    def clean_paths():
        shutil.rmtree("media/screenshots")

    @staticmethod
    def __generate_random_id():
        n = 10
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

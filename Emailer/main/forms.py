from abc import ABC

from django import forms

from Emailer.authentication.models import CustomUserModel
from Emailer.main.models import Receiver, Preferences, Group, Email
from Emailer.main.utils import Sender


class ReceiverForm(forms.ModelForm):
    preferences = forms.ModelMultipleChoiceField(queryset=Preferences.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["preferences"].choices = \
            [(choice, choice) for choice in Preferences.objects.all().values_list("hobby", flat=True)]

    class Meta:
        model = Receiver
        fields = ("email", "first_name", "last_name", "age", "preferences")
        widgets = {
            "email": forms.EmailInput(attrs={
                "type": "text", "class": 'form-control', "required": True, "placeholder": "Enter Mail"
            }),
            "preferences": forms.SelectMultiple(attrs={
                "type": "text", "class": 'form-control',
            }),
            "first_name": forms.TextInput(attrs={
                "type": "text", "class": 'form-control', "placeholder": "Enter First Name"
            }),
            "last_name": forms.TextInput(attrs={
                "type": "text", "class": 'form-control', "placeholder": "Enter Last Name"
            }),
            "age": forms.NumberInput(attrs={
                "type": "number", "class": 'form-control', "placeholder": "Enter Age", "name": "age"
            }),
        }

        labels = {
            "mail": "Mail:",
            "preferences": "Preference:",
            "first_name": "First Name:",
            "last_name": "Last Name:",
            "age": "Age:"
        }


class GroupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["receivers"].choices = \
            [(choice, choice) for choice in Receiver.objects.all().values_list("mail", flat=True)]

    class Meta:
        model = Group
        fields = ("name", "receivers")
        widgets = {
            "receivers": forms.CheckboxSelectMultiple(attrs={
                "class": 'form-control',
            }),
            "name": forms.TextInput(attrs={
                "type": "text", "class": 'form-control', "placeholder": "Enter Group Name"
            }),
        }


class SendMailForm(forms.Form):
    """
    This form is to authenticate all the entries
    """
    email = forms.EmailField()
    message = forms.CharField(max_length=250)
    subject = forms.CharField(max_length=20)
    template = forms.CharField(max_length=20)

    def save(self, sender: CustomUserModel):
        receiver = Receiver(email=self.cleaned_data["email"])
        subject = self.cleaned_data["subject"]
        message = self.cleaned_data["message"]
        template = self.cleaned_data["template"]
        receiver.save()
        sender_class_instance = Sender.get_instance()
        sender_class_instance.send_single_mail(subject, message, sender, receiver, template)
        Email()

from django import forms
from django.core.exceptions import ValidationError

from Emailer.authentication.models import CustomUserModel
from Emailer.main.models import Receiver, Preferences, Group, CustomTemplate
from Emailer.main.utils import EmailDispatcher


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
            [(choice, choice) for choice in Receiver.objects.all().values_list("email", flat=True)]

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


class SendEmailForm(forms.Form):
    """
    This form is to authenticate all the entries
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "placeholder": "Enter email", "class": "form-control"
    }), label="Enter Email")
    subject = forms.CharField(max_length=250, widget=forms.TextInput(attrs={
        "placeholder": "Enter Subject", "class": "form-control"
    }), label="Enter Subject")
    template = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Choose template", "class": "form-control", "id": "template-input",
    }), label="Choose template from the right menu")
    message = forms.CharField(max_length=20, widget=forms.Textarea(attrs={
        "placeholder": "Enter content"
    }))

    def clean_template(self):
        try:
            value = CustomTemplate.objects.get(template__exact=self.cleaned_data["template"])
        except ValueError:
            raise ValidationError("Template doesn't exist")
        return value

    def save(self, sender: CustomUserModel):
        receiver = self.create_receiver(sender)
        subject = self.cleaned_data["subject"]
        message = self.cleaned_data["message"]
        template = self.cleaned_data["template"]
        dispatcher = EmailDispatcher(
            subject=subject,
            message=message,
            sender=sender,
            receivers=[receiver],
            template=template
        )
        dispatcher.send_single_mail()

    def create_receiver(self, sender: CustomUserModel):
        (receiver, created) = Receiver.objects.get_or_create(email=self.cleaned_data["email"])
        if created:
            receiver.user = sender
        return receiver

from django import forms
from django.core.exceptions import ValidationError
from Emailer.authentication.models import CustomUserModel
from Emailer.main.models import Receiver, Preferences, Group, CustomTemplate
from Emailer.main.utils import EmailDispatcher


class GenericManyToManyForm(forms.ModelForm):
    def __init__(self, *args, user=None,  **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    unique_arg = None

    class Meta:
        model = None
        fields = None

    def clean(self):
        unique_data = self.cleaned_data[self.unique_arg]
        instance = self.check_if_exists(unique_data)
        if instance is not None:
            self.instance = instance
        super().clean()

    def check_if_exists(self, unique_entry):
        """
        check if unique entry exists in model
        :return: Model instance or None
        """
        return None

    def save(self, commit=True):
        if self.instance and self.instance.id is not None:
            self.instance.delete()
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class ReceiverForm(GenericManyToManyForm):
    preferences = forms.ModelMultipleChoiceField(queryset=Preferences.objects.all())
    unique_arg = "email"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["preferences"].choices = \
            [(choice, choice) for choice in Preferences.objects.all().values_list("hobby", flat=True)]

    class Meta(GenericManyToManyForm.Meta):
        model = Receiver
        fields = ("email", "first_name", "last_name", "age", "preferences")
        widgets = {
            "email": forms.EmailInput(attrs={
                "type": "text", "class": 'form-control', "required": True, "placeholder": "Enter Mail"
            }),
            "preferences": forms.SelectMultiple(attrs={
                "class": 'form-control',
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

    def check_if_exists(self, unique_entry):
        try:
            return Receiver.objects.filter(user=self.user, email__exact=unique_entry)[0]
        except IndexError:
            return None


class GroupForm(GenericManyToManyForm):
    unique_arg = "name"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["receivers"].choices = \
            [(choice, choice) for choice in Receiver.objects.all().values_list("email", flat=True)]

    class Meta(GenericManyToManyForm.Meta):
        model = Group
        fields = ("name", "receivers")
        widgets = {
            "receivers": forms.SelectMultiple(attrs={
                "class": 'form-control',
            }),
            "name": forms.TextInput(attrs={
                "type": "text", "class": 'form-control', "placeholder": "Enter Group Name"
            }),
        }

    def check_if_exists(self, unique_entry):
        try:
            return Group.objects.filter(receivers__user_id__exact=self.user, name__exact=unique_entry)[0]
        except IndexError:
            return None


class GenericSendEmailForm(forms.Form):
    """
    This is base form for Send email forms
    """
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

    def save(self, *args):
        """
        This function must be overritten
        :return: void
        """

    def get_kwargs(self):
        return {
            "subject": self.cleaned_data["subject"],
            "message": self.cleaned_data["message"],
            "template": self.cleaned_data["template"]
        }


class SendSingleEmailForm(GenericSendEmailForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "placeholder": "Enter email", "class": "form-control"
    }), label="Enter Email")

    def save(self, sender, pk=None):
        receiver = self.create_receiver(sender)
        dispatcher = EmailDispatcher(
            sender=sender,
            receivers=[receiver],
            **self.get_kwargs()
        )
        dispatcher.send_single_mail()

    def create_receiver(self, sender: CustomUserModel):
        (receiver, created) = Receiver.objects.get_or_create(email=self.cleaned_data["email"])
        if created:
            receiver.user = sender
            receiver.save()
        return receiver


class SendMassEmailForm(GenericSendEmailForm):
    def save(self, sender, group_id):
        receivers = Group.objects.get(id=group_id).receivers.all()

        dispatcher = EmailDispatcher(
            receivers=receivers,
            **self.get_kwargs(),
            sender=sender
        )

        dispatcher.send_mass_mail()


class FilterForm(ReceiverForm):
    class Meta(ReceiverForm.Meta):
        fields = ("preferences",)

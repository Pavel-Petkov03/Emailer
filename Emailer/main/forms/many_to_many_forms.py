from django import forms
from Emailer.main.forms.base_forms import BaseManyToManyForm
from Emailer.main.models import Preferences, Receiver, Group


class ReceiverForm(BaseManyToManyForm):
    preferences = forms.ModelMultipleChoiceField(queryset=Preferences.objects.all())
    unique_arg = "email"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["preferences"].choices = \
            [(choice, choice) for choice in Preferences.objects.all().values_list("hobby", flat=True)]

    class Meta(BaseManyToManyForm.Meta):
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


class GroupForm(BaseManyToManyForm):
    unique_arg = "name"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["receivers"].choices = \
            [(choice, choice) for choice in Receiver.objects.all().values_list("email", flat=True)]

    class Meta(BaseManyToManyForm.Meta):
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

from django import forms

from Emailer.main.models import Receiver, Preferences, Group


class ReceiverForm(forms.ModelForm):
    preferences = forms.ModelMultipleChoiceField(queryset=Preferences.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["preferences"].choices = \
            [(choice, choice) for choice in Preferences.objects.all().values_list("hobby", flat=True)]

    class Meta:
        model = Receiver
        fields = ("mail", "first_name", "last_name", "age", "preferences")
        widgets = {
            "mail": forms.EmailInput(attrs={
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
    receiver = forms.ModelMultipleChoiceField(queryset=Preferences.objects.all())

    class Meta:
        model = Group
        fields = ("name", "receivers")
        widgets = {
            "receivers": forms.SelectMultiple(attrs={
                "type": "text", "class": 'form-control',
            }),
            "name": forms.TextInput(attrs={
                "type": "text", "class": 'form-control', "placeholder": "Enter Group Name"
            }),
        }

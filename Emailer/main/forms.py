from django import forms

from Emailer.main.models import Receiver


class ReceiverForm(forms.ModelForm):
    class Meta:
        model = Receiver
        fields = "__all__"
        widgets = {
            "preferences": forms.SelectMultiple(attrs={
                "type": "text", "class": 'form-control', "placeholder": "Enter Username"
            }),
            "first_name": forms.TextInput(),
            "last_name": forms.TextInput(),
            "age": forms.NumberInput(),
        }

        labels = {
            "preferences": "Preference:",
            "first_name": "First Name:",
            "last_name": "Last Name:",
            "age": "Age:"
        }

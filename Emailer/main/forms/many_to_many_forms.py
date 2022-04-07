from django import forms
from Emailer.main.forms.base_forms import BaseManyToManyForm
from Emailer.main.models import Preferences, Receiver, Group


class ReceiverForm(BaseManyToManyForm):

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

    def save(self, commit=True):
        try:
            instance = Receiver.objects.get(email__exact=self.cleaned_data["email"], user__exact=self.user)
            for preference in instance.preferences.all():
                instance.preferences.remove(preference)
            instance.__dict__.update(self.cleaned_data)
            instance.preferences.add(*self.cleaned_data["preferences"])
            instance.save()
        except Receiver.DoesNotExist:
            many_to_many_arg = self.cleaned_data.pop("preferences")
            instance = Receiver(**self.cleaned_data, user=self.user)
            instance.save()
            instance.preferences.add(*many_to_many_arg)
            instance.save()


class GroupForm(BaseManyToManyForm):
    unique_arg = "name"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["receivers"].choices = \
            [(choice, choice) for choice in Receiver.objects.filter(user__exact=self.user).values_list("email", flat=True)]

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

    def save(self, commit=True):
        try:
            instance = Group.objects.get(
                name__exact=self.cleaned_data["name"],
                receivers__user__exact=self.user
            ).distinct()
            for receiver in instance.receivers.all():
                instance.receivers.remove(receiver)
            instance.__dict__.update(self.cleaned_data)
            instance.receivers.add(*self.cleaned_data["receivers"])
            instance.save()
        except Group.DoesNotExist:
            many_to_many_arg = self.cleaned_data.pop("receivers")
            instance = Group(**self.cleaned_data)
            instance.save()
            instance.receivers.add(*many_to_many_arg)
            instance.save()

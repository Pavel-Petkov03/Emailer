from django import forms
from django.core.exceptions import ValidationError

from Emailer.main.models import CustomTemplate


class BaseManyToManyForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
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


class BaseSendEmailForm(forms.Form):
    """
    This is views form for Send email forms
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
        except :
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

from django import forms
from django.core.exceptions import ValidationError

from Emailer.main.models import CustomTemplate


class BaseManyToManyForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = None
        fields = None






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
        except:
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

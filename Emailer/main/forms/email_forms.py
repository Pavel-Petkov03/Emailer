from django import forms
from Emailer.authentication.models import CustomUserModel
from Emailer.main.forms.base_forms import BaseSendEmailForm
from Emailer.main.models import Receiver, Group
from Emailer.main.utils import EmailDispatcher


class SendSingleEmailForm(BaseSendEmailForm):
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


class SendMassEmailForm(BaseSendEmailForm):
    def save(self, sender, group_id):
        receivers = Group.objects.get(id=group_id).receivers.all()

        dispatcher = EmailDispatcher(
            receivers=receivers,
            **self.get_kwargs(),
            sender=sender
        )

        dispatcher.send_mass_mail()

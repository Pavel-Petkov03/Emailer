from datetime import datetime, timedelta

from Emailer.main.models import Email, Receiver
from rest_framework import serializers


class GenericFolderSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    date = serializers.DateTimeField()
    template = serializers.CharField(source="template.name")
    receiver = serializers.CharField(source="receiver.email")

    class Meta:
        model = Email
        fields = ["receiver", "subject", "date", "template", "id"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        current_date = instance.date + timedelta(hours=3)
        if current_date.date() == datetime.today().date():
            fm = "%H:%M"
        else:
            fm = "%d.%m.%y"
        representation["date"] = current_date.strftime(fm)
        return representation


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("email",)
        model = Receiver


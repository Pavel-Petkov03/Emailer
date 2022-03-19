from datetime import datetime

from Emailer.main.models import Email
from rest_framework import serializers


class GenericFolderSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    date = serializers.DateTimeField()
    template = serializers.CharField(source="template.template")
    receiver = serializers.CharField(source="receiver.email")

    class Meta:
        model = Email
        fields = ["receiver", "subject", "date", "template", "id"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        current_date = instance.date
        if current_date.today() == datetime.today():
            fm = "%H:%M"
        else:
            fm = "%d:%m:%y"
        representation["date"] = current_date.strftime(fm)
        return representation

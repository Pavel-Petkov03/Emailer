from rest_framework import serializers

from Emailer.main.models import Email
from datetime import datetime


class GenericFolderSerializer(serializers.ModelSerializer):
    date = serializers.DateField(default=datetime.now().strftime("%H:%M:%S"))

    class Meta:
        model = Email
        fields = ["receiver", "subject", "date", "template"]

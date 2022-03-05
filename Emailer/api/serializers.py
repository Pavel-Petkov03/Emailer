from datetime import datetime

from Emailer.main.models import Email
from rest_framework import serializers


class GenericFolderSerializer(serializers.ModelSerializer):
    date = serializers.DateField(default=datetime.now().strftime("%H:%M:%S"))

    class Meta:
        model = Email
        fields = ["receiver", "subject", "date", "template"]

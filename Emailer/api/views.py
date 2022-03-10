from abc import ABC, abstractmethod

from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from Emailer.api.serializers import GenericFolderSerializer
from Emailer.main.models import Receiver, Email


class GenericFolder(ListAPIView, ABC):
    """
    This class will be abstract
    It will be used for Folder view and Bin view
    """

    permission_classes = [IsAuthenticated]
    serializer_class = GenericFolderSerializer
    deleted = False
    allowed_filtering_strings = ["subject", "creation date", "template", "receiver"]

    def get_queryset(self):
        try:
            kwarg = list(self.request.GET.dict())[0]
            if kwarg not in self.allowed_filtering_strings:
                raise ValueError('the filter params must match the allowed filtering params')
        except [IndexError, ValueError]:
            kwarg = "subject"
        return Email.objects.filter(receiver__user__id=self.request.user.id, is_deleted=self.deleted).order_by(kwarg)


class Folder(GenericFolder):
    deleted = False


class Bin(GenericFolder):
    deleted = True


class Ser(serializers.ModelSerializer):
    receiver = serializers.CharField(source="receiver.mail")

    class Meta:
        fields = ("receiver", "subject", "date",)
        model = Email


class GroupView(ListCreateAPIView):
    serializer_class = Ser
    permission_classes = [IsAuthenticated]

from abc import ABC, abstractmethod

from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from Emailer.api.serializers import GenericFolderSerializer
from Emailer.main.models import Email


class GenericFolder(ListAPIView, ABC):
    """
    This class will be abstract
    It will be used for Folder view and Bin view
    """

    permission_classes = [IsAuthenticated]
    serializer_class = GenericFolderSerializer
    deleted = False
    allowed_filtering_strings = ["subject", "date", "template", "receiver"]

    @abstractmethod
    def get_queryset(self):
        try:
            kwarg = self.request.GET.dict()["kwarg"]
            if kwarg not in GenericFolder.allowed_filtering_strings:
                raise ValueError('the filter params must match the allowed filtering params')
        except KeyError as error:
            kwarg = "subject"
        except ValueError:
            kwarg = "subject"
        return Email.objects.filter(receiver__user=self.request.user, is_deleted=self.deleted).order_by(kwarg)


class Folder(GenericFolder):
    deleted = False

    def get_queryset(self):
        return super().get_queryset()


class Bin(GenericFolder):
    deleted = True

    def get_queryset(self):
        return super().get_queryset()


class Ser(serializers.ModelSerializer):
    receiver = serializers.CharField(source="receiver.mail")

    class Meta:
        fields = ("receiver", "subject", "date",)
        model = Email


class GroupView(ListCreateAPIView):
    serializer_class = Ser
    permission_classes = [IsAuthenticated]

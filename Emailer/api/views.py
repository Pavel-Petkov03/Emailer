from abc import ABC, abstractmethod

from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer

from Emailer.api.serializers import GenericFolderSerializer
from Emailer.main.models import Receiver


class GenericFolder(ListAPIView, ABC):
    """
    This class will be abstract
    It will be used for Folder view and Bin view
    """

    permission_classes = [IsAuthenticated]
    serializer_class = GenericFolderSerializer
    deleted = False

    def list(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.list(request, *args, **kwargs)

    def get_queryset(self):
        """
        This function will be overridden if you need take make filtering with params
        :return: QuerySet
        """
        return super().get_queryset()


class Folder(GenericFolder):
    deleted = False


class Bin(GenericFolder):
    deleted = True


class Ser(ModelSerializer):
    class Meta:
        fields = ("mail", "first_name", "last_name")
        model = Receiver


class GroupView(ListCreateAPIView):
    serializer_class = Ser
    queryset = Receiver.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pass

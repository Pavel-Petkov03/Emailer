from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from Emailer.api.serializers import GenericFolderSerializer


class GenericFolder(ListAPIView):
    """
    This class won't be abstract
    It will be used for Folder view and Bin view
    """

    permission_classes = [IsAuthenticated]
    serializer_class = GenericFolderSerializer
    deleted = False

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        self.serializer_class(queryset, many=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return 1


class Folder(GenericFolder):
    deleted = False


class Bin(GenericFolder):
    deleted = True


class GroupView(ListCreateAPIView):
    serializer_class = None

    def post(self, request, *args, **kwargs):
        pass

    def get_queryset(self):
        print(12)
        return 12




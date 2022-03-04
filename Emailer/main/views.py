from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from Emailer.main.serializers import GenericFolderSerializer


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
        self.serializer_class(queryset, manu=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return 1


class Folder(GenericFolder):
    deleted = False


class Bin(GenericFolder):
    deleted = True

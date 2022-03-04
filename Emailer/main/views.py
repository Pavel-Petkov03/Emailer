from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


class Folder(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = 1

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        self.serializer_class(queryset, manu=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        pass





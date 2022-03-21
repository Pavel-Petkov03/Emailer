

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Emailer.api.serializers import GenericFolderSerializer, FilterSerializer
from Emailer.main.models import Email, Receiver, Preferences


class GenericFolder(ListAPIView):
    """
    This class will be abstract
    It will be used for Folder view and Bin view
    """

    permission_classes = [IsAuthenticated]
    serializer_class = GenericFolderSerializer
    allowed_filtering_strings = ["subject", "date", "template", "receiver"]

    def get_queryset(self):
        deleted = None
        try:
            filter_dict = self.request.GET.dict().copy()
            kwarg = filter_dict["kwarg"]
            is_bin = filter_dict["isbin"]
            deleted = True if is_bin == str(True) else False
            if kwarg not in GenericFolder.allowed_filtering_strings:
                raise ValueError('the filter params must match the allowed filtering params')
        except KeyError as error:
            kwarg = "subject"
        except ValueError:
            kwarg = "subject"
        return Email.objects.filter(receiver__user=self.request.user, is_deleted=deleted).order_by(kwarg)


class FilterEmail(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, req):
        min_value = req.data.get("min_age")
        max_value = req.data.get("max_age")
        preferences = req.data.get("preferences")

        data = Receiver.objects.filter(
            preferences__in=Preferences.objects.filter(hobby__in=preferences),
            user=req.user,
            age__gte=min_value,
            age__lte=max_value,
        )

        serializer = FilterSerializer(data, many=True)
        return Response(serializer.data)

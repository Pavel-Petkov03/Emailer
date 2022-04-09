from rest_framework import status
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

    serializer_class = GenericFolderSerializer
    allowed_filtering_strings = ["subject", "date", "template", "receiver"]
    permission_classes = [IsAuthenticated]

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
    """make query for receivers from filter form"""
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


class DeleteEmailView(APIView):
    """
    delete email with api view
    """

    def delete(self, request, pk):
        try:
            current_email = Email.objects.get(
                receiver__user=request.user,
                id=pk)
            place = request.GET.dict()["place"]
            if place == "folder":
                current_email.is_deleted = True
                current_email.save()
            else:
                current_email.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Email.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DeleteReceiverView(APIView):
    """delete receiver with api view"""

    def delete(self, request, pk):
        try:
            current_receiver = Receiver.objects.get(id=pk, user=request.user)
            current_receiver.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Receiver.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

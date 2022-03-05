from django.shortcuts import render, redirect
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.views import View
from Emailer.main.models import Receiver, Preferences
from Emailer.main.forms import ReceiverForm
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


class ReceiverView(View):
    def get(self, req):
        form = ReceiverForm()
        return render(req, "add_receiver.html", {
            "form": form
        })

    def post(self, req, ):
        post_data = req.POST.copy()
        post_data.setlist("preferences", self.extract_preferences(req.POST.getlist("preferences")))
        form = ReceiverForm(post_data)
        if form.is_valid():
            receiver = form.save(commit=False)
            receiver.user = req.user
            receiver.save()
            form.save_m2m()
            return redirect("/")
        return render(req, "add_receiver.html", {
            "form": form
        })

    @staticmethod
    def extract_preferences(preferences: list):
        return [str(preference.id) for preference in Preferences.objects.filter(hobby__in=preferences)]

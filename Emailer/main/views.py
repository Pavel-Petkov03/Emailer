from django.shortcuts import render, redirect
from django.views import View
from Emailer.main.models import Preferences
from Emailer.main.forms import ReceiverForm


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

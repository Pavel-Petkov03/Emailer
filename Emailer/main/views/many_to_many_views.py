from django.shortcuts import render

from Emailer.main.forms.many_to_many_forms import ReceiverForm, GroupForm
from Emailer.main.models import Receiver, Preferences
from Emailer.main.views.base_views import BaseManyToManyView


class ReceiverView(BaseManyToManyView):
    form_class = ReceiverForm
    template = "add_receiver.html"
    many_to_many_argument = "preferences"
    success_url = "folder"

    def convert_from_many_to_many_arg_to_id(self, *args):
        return [str(preference.id) for preference in Preferences.objects.filter(hobby__in=args[0])]


class GroupView(BaseManyToManyView):
    form_class = GroupForm
    template = "add_group.html"
    many_to_many_argument = "receivers"
    success_url = "folder"

    def get(self, req):
        form = self.form_class(user=req.user)
        filter_form = FilterForm()
        return render(req, self.template, {
            "form": form,
            "filter_form": filter_form
        })

    def convert_from_many_to_many_arg_to_id(self, array_of_fields, user):
        return [str(receiver.id) for receiver in Receiver.objects.filter(email__in=array_of_fields, user_id=user)]


class FilterForm(ReceiverForm):
    class Meta(ReceiverForm.Meta):
        fields = ("preferences",)



def home(request):
    return render(request, "home.html")

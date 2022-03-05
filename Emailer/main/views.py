from django.shortcuts import render, redirect
from django.views import View
from Emailer.main.models import Preferences
from Emailer.main.forms import ReceiverForm


class ManyToManyModelCustomView(View):
    form_class = None
    template = None
    many_to_many_argument = None
    success_url = None
    query_keyword = None

    def get(self, req):
        form = self.form_class()
        return render(req, self.template, {
            "form": form
        })

    def post(self, req):
        post_data = req.POST.copy()
        post_data.setlist(self.many_to_many_argument, self.extract_preferences())
        form = self.form_class(post_data)
        if form.is_valid:
            custom_model_field = form.save(commit=False)
            custom_model_field.user = req.user
            custom_model_field.save()
            form.save_m2m()
            return redirect(self.success_url)

        return render(req, self.template, {
            "form": form
        })

    def extract_preferences(self):
        """

        :return: array with id's which will be saved via save_m2m()
        this function could be overridden
        """
        return [str(arg.id) for arg in
                self.form_class.model.objects.filter(**self.query_param_getter())]

    def query_param_getter(self):
        context = dict()
        context[self.get_variable_name(self.many_to_many_argument)] = self.many_to_many_argument
        return context

    @staticmethod
    def get_variable_name(variable):
        return [k for k, v in locals().items() if v == variable][0]


class ReceiverView(ManyToManyModelCustomView):
    form_class = ReceiverForm
    template = "add_receiver.html"
    many_to_many_argument = "preferences"
    success_url = "login"
    query_keyword = "hobby__in"


class GroupView(ManyToManyModelCustomView):
    pass

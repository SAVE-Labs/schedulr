from django.contrib.auth import get_user_model
from django.contrib.auth.views import RedirectURLMixin
from django.urls import reverse_lazy
from django.views.generic import edit

from .forms import InitialSetupForm, SessionSetupForm

User = get_user_model()


# Create your views here.
class InitialSetupView(edit.FormView):
    template_name = "account/initial_setup.html"
    form_class = InitialSetupForm
    success_url = reverse_lazy("admin:login")

    def form_valid(self, form):
        User.objects.create_superuser(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )
        return super().form_valid(form)


class SessionSetupView(RedirectURLMixin, edit.FormView):
    next_page = "homepage"
    template_name = "account/session_setup.html"
    form_class = SessionSetupForm

    def form_valid(self, form):
        self.request.session["name"] = form.cleaned_data["name"].lower()
        return super().form_valid(form)

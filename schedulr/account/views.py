from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, edit

from .forms import InitialSetupForm
from .mixins import InitialSetupRequiredMixin, SetupCompletedMixin

User = get_user_model()


# Create your views here.
class InitialSetupView(SetupCompletedMixin, edit.FormView):
    template_name = "account/initial_setup.html"
    form_class = InitialSetupForm
    success_url = "login"

    def form_valid(self, form):
        User.objects.create_user(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )
        return super().form_valid(form)


class LoginView(InitialSetupRequiredMixin, auth_views.LoginView):
    template_name = "account/login.html"


class LogoutView(auth_views.LogoutView):
    pass


class Homepage(LoginRequiredMixin, TemplateView):
    template_name = "page.html"

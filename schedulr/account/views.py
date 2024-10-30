from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import edit

from .forms import InitialSetupForm

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

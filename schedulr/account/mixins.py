from django.contrib.auth import get_user_model
from django.shortcuts import redirect

User = get_user_model()


class InitialSetupRequiredMixin:
    initial_setup_url = "initial-setup"

    def dispatch(self, request, *args, **kwargs):
        if not User.objects.exists():
            return redirect(self.initial_setup_url)
        return super().dispatch(request, *args, **kwargs)


class SetupCompletedMixin:
    setup_completed_url = "login"

    def dispatch(self, request, *args, **kwargs):
        if User.objects.exists():
            return redirect(self.setup_completed_url)
        return super().dispatch(request, *args, **kwargs)

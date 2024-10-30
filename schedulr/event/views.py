from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, TemplateView

from .models import Event, ScheduleOption


class Homepage(TemplateView):
    template_name = "event/event_create.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        description = request.POST.get("description")
        schedule_options = request.POST.getlist("schedule_options[]")

        event = Event.objects.create(name=name, description=description)

        for option in schedule_options:
            ScheduleOption.objects.create(event=event, option=option)

        return redirect(reverse("event_detail", args=(event.pk,)))

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class EventDetail(DetailView):
    template_name = "event/event_detail.html"
    queryset = Event.objects.all()

    def get(self, request, *args, **kwargs):
        if not request.session.get("name"):
            path = request.get_full_path()
            return redirect_to_login(path, "whoami")
        return super().get(request, *args, **kwargs)

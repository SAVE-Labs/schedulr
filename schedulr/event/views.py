from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from .models import Event, ScheduleOption


class Homepage(LoginRequiredMixin, TemplateView):
    template_name = "event/event_create.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        description = request.POST.get('description')
        schedule_options = request.POST.getlist('schedule_options[]')

        event = Event.objects.create(name=name, description=description)

        for option in schedule_options:
            ScheduleOption.objects.create(event=event, option=option)

        return redirect('homepage')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

from django.contrib.auth.views import redirect_to_login
from django.forms import formset_factory
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, TemplateView

from .forms import SelectOptionForm
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

        SelectOptionFormSet = formset_factory(SelectOptionForm, extra=0)
        self.object = self.get_object()

        form_data = []
        for option in self.object.scheduleoption_set.all():
            form_data.append(
                {
                    "option": option,
                    "timestamp": option.option,
                }
            )

        formset = SelectOptionFormSet(initial=form_data)

        context = self.get_context_data(object=self.object)

        context["formset"] = formset

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # TODO: Mixin?
        if not request.session.get("name"):
            path = request.get_full_path()
            return redirect_to_login(path, "whoami")

        name = request.session.get("name")
        self.object = self.get_object()

        SelectOptionFormSet = formset_factory(SelectOptionForm)

        formset = SelectOptionFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data["choice"] != "no":
                    from .models import Invitee, SelectedOption

                    SelectedOption.objects.create(
                        option=form.cleaned_data["option"],
                        invitee=Invitee.objects.get_or_create(
                            name=name, event=self.object
                        )[0],
                        tentative=form.cleaned_data["choice"] == "tentative",
                    )

            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        print(formset.errors)

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

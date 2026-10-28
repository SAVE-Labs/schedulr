from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, TemplateView

from schedulr.account.mixins import InitialSetupRequiredMixin

from .forms import SelectOptionForm
from .models import Event, Invitee, ScheduleOption, SelectedOption


class NameRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed

        if handler == self.http_method_not_allowed:
            return handler

        if not request.session.get("name"):
            path = request.get_full_path()
            return redirect_to_login(path, "whoami")

        return handler(request, *args, **kwargs)


def can_edit_event(request, event):
    return event.pk in request.session.get("created_events", [])


class Homepage(InitialSetupRequiredMixin, TemplateView):
    template_name = "event/event_create.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        description = request.POST.get("description")
        schedule_options = request.POST.getlist("schedule_options[]")

        event = Event.objects.create(name=name, description=description)

        for option in schedule_options:
            ScheduleOption.objects.create(event=event, option=option)

        # Only the browser session that created the event may edit it
        request.session["created_events"] = [
            *request.session.get("created_events", []),
            event.pk,
        ]

        return redirect(reverse("event_detail", args=(event.pk,)))

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class EventEdit(NameRequiredMixin, TemplateView):
    template_name = "event/event_create.html"

    def _context(self, event):
        return {
            "event": event,
            "options": event.scheduleoption_set.all().order_by("option"),
        }

    def get(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs["pk"])
        if not can_edit_event(request, event):
            raise PermissionDenied
        return render(request, self.template_name, self._context(event))

    def post(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs["pk"])
        if not can_edit_event(request, event):
            raise PermissionDenied
        event.name = request.POST.get("name")
        event.description = request.POST.get("description")
        event.save()

        option_ids = request.POST.getlist("option_ids[]")
        schedule_options = request.POST.getlist("schedule_options[]")

        # Existing options are updated in place so their votes are kept,
        # options that were removed from the form are deleted.
        kept = []
        for option_id, value in zip(option_ids, schedule_options):
            if option_id:
                option = get_object_or_404(ScheduleOption, pk=option_id, event=event)
                option.option = value
                option.save()
            else:
                option = ScheduleOption.objects.create(event=event, option=value)
            kept.append(option.pk)
        event.scheduleoption_set.exclude(pk__in=kept).delete()

        return redirect(reverse("event_detail", args=(event.pk,)))


class EventDetail(NameRequiredMixin, DetailView):
    template_name = "event/event_detail.html"
    queryset = Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_edit"] = can_edit_event(self.request, self.object)
        return context

    def _build_formset_data(self):
        form_data = []

        for option in self.object.scheduleoption_set.all().order_by("option"):
            option_data = {}
            option_data["option"] = option
            selected_option = option.selectedoption_set.filter(
                invitee__name=self.name_in_session
            ).first()
            if selected_option:
                option_data["choice"] = (
                    "tentative" if selected_option.tentative else "yes"
                )
            form_data.append(option_data)

        return form_data

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.name_in_session = request.session.get("name")

        SelectOptionFormSet = formset_factory(SelectOptionForm, extra=0)

        formset = SelectOptionFormSet(initial=self._build_formset_data())

        context = self.get_context_data(object=self.object)
        context["formset"] = formset

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.name_in_session = request.session.get("name")
        self.object = self.get_object()

        SelectOptionFormSet = formset_factory(SelectOptionForm, extra=0)

        formset = SelectOptionFormSet(
            request.POST, request.FILES, initial=self._build_formset_data()
        )

        context = self.get_context_data(object=self.object)
        context["formset"] = formset

        if formset.is_valid():
            invitee, created = Invitee.objects.get_or_create(
                name=self.name_in_session, event=self.object
            )
            for form in formset:
                if form.cleaned_data["choice"] != "no":
                    SelectedOption.objects.update_or_create(
                        option=form.cleaned_data["option"],
                        invitee=invitee,
                        defaults={
                            "tentative": form.cleaned_data["choice"] == "tentative",
                        },
                    )
                else:
                    SelectedOption.objects.filter(
                        option=form.cleaned_data["option"],
                        invitee=invitee,
                    ).delete()

        return self.render_to_response(context)

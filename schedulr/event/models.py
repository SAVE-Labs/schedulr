from django.db import models

from .utils import generate_unique_id


class Event(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_unique_id,
        editable=False,
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    # TODO: Event creator?


class ScheduleOption(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    option = models.DateTimeField()

    def selected_context(self):
        selected_by = self.selectedoption_set.all().select_related("invitee")
        context = {
            "yes": [],
            "tentative": [],
        }
        for selected in selected_by:
            invitee_name = selected.invitee.name
            if selected.tentative:
                context["tentative"].append(invitee_name)
            else:
                context["yes"].append(invitee_name)

        return context


class Invitee(models.Model):
    name = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class SelectedOption(models.Model):
    option = models.ForeignKey(ScheduleOption, on_delete=models.CASCADE)
    invitee = models.ForeignKey(Invitee, on_delete=models.CASCADE)
    tentative = models.BooleanField(default=False)

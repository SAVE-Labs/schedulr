from django.db import models
from django.utils import timezone

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
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.id})"


class ScheduleOption(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    option = models.DateTimeField()

    def selected_context(self):
        selected_by = self.selectedoption_set.all().select_related("invitee")
        context = {
            "yes": [],
            "tentative": [],
            "no": [],
        }
        for selected in selected_by:
            invitee_name = selected.invitee.name
            if selected.declined:
                context["no"].append(invitee_name)
            elif selected.tentative:
                context["tentative"].append(invitee_name)
            else:
                context["yes"].append(invitee_name)

        return context

    def is_past(self):
        return self.option.date() < timezone.now().date()

    def yes_count(self):
        return self.selectedoption_set.filter(tentative=False, declined=False).count()

    def is_top_3(self):
        options = ScheduleOption.objects.filter(event=self.event)
        sorted_options = sorted(options, key=lambda o: o.yes_count(), reverse=True)
        top_3 = sorted_options[:3]
        return self in top_3


class Invitee(models.Model):
    name = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class SelectedOption(models.Model):
    option = models.ForeignKey(ScheduleOption, on_delete=models.CASCADE)
    invitee = models.ForeignKey(Invitee, on_delete=models.CASCADE)
    tentative = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)

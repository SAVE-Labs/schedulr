from django.contrib import admin

from .models import Event, Invitee, ScheduleOption, SelectedOption

admin.site.register(Event)
admin.site.register(Invitee)
admin.site.register(SelectedOption)
admin.site.register(ScheduleOption)

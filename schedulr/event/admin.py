from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Event, Invitee, ScheduleOption, SelectedOption


@admin.register(Event)
class EventAdmin(ModelAdmin):
    pass


@admin.register(Invitee)
class InviteeAdmin(ModelAdmin):
    pass


@admin.register(SelectedOption)
class SelectedOptionAdmin(ModelAdmin):
    pass


@admin.register(ScheduleOption)
class ScheduleOptionAdmin(ModelAdmin):
    pass

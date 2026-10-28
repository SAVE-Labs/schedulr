from django.contrib import admin
from django.db.models import Count, F, Min
from unfold.admin import ModelAdmin

from .models import Event, Invitee, ScheduleOption, SelectedOption


class ScheduleOptionInline(admin.TabularInline):
    model = ScheduleOption


class HasAnswersFilter(admin.SimpleListFilter):
    title = "answers"
    parameter_name = "answers"

    def lookups(self, request, model_admin):
        return [
            ("yes", "Has answers"),
            ("no", "No answers"),
            ("all", "All"),
        ]

    def choices(self, changelist):
        value = self.value() or "yes"
        for lookup, title in self.lookup_choices:
            yield {
                "selected": value == lookup,
                "query_string": changelist.get_query_string({self.parameter_name: lookup}),
                "display": title,
            }

    def queryset(self, request, queryset):
        value = self.value() or "yes"
        if value == "yes":
            return queryset.filter(answer_count__gt=0)
        if value == "no":
            return queryset.filter(answer_count=0)
        return queryset


@admin.register(Event)
class EventAdmin(ModelAdmin):
    inlines = [ScheduleOptionInline]
    list_display = ['name', 'answers', 'dates', 'first_date', 'created_at', 'id']
    list_filter = [HasAnswersFilter]
    search_fields = ['name', 'description']
    ordering = [F('created_at').desc(nulls_last=True), 'name']

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                answer_count=Count('invitee', distinct=True),
                date_count=Count('scheduleoption', distinct=True),
                first_option=Min('scheduleoption__option'),
            )
        )

    @admin.display(description='Answers', ordering='answer_count')
    def answers(self, obj):
        return obj.answer_count

    @admin.display(description='Dates', ordering='date_count')
    def dates(self, obj):
        return obj.date_count

    @admin.display(description='First date', ordering='first_option')
    def first_date(self, obj):
        return obj.first_option


@admin.register(Invitee)
class InviteeAdmin(ModelAdmin):
    pass


@admin.register(SelectedOption)
class SelectedOptionAdmin(ModelAdmin):
    pass


@admin.register(ScheduleOption)
class ScheduleOptionAdmin(ModelAdmin):
    pass

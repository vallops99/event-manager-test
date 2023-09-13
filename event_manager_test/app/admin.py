"""Admin module to setup admin panel."""
from django.contrib import admin

from event_manager_test.app.models import Event


class EventAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "start_datetime",
        "end_datetime",
        "registered_users",
        "e_type"
    )
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Event, EventAdmin)

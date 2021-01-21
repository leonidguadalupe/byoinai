from django.contrib import admin
from api.models import Sync


class SyncAdmin(admin.ModelAdmin):
    list_display = ('created_date', 'status', 'reason')
    ordering = ('-created_date',)


admin.site.register(Sync, SyncAdmin)

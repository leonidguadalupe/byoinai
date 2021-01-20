from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from api.models import Sync

class SyncAdmin(admin.ModelAdmin):
    list_display = ('created_date', 'status', 'reason')
    ordering = ('-created_date',)

admin.site.register(Sync, SyncAdmin)
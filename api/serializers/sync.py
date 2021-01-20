import os

from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers

from api.models import Sync

class SyncSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sync
        fields = ['created_date', 'status', 'reason']

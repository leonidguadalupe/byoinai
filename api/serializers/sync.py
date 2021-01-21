from rest_framework import serializers

from api.models import Sync


class SyncSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sync
        fields = ['created_date', 'status', 'reason']

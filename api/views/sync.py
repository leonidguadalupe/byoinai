"""
.. module:: sync
   :synopsis: Endpoints for sync functionalities
.. moduleauthor:: Leonid Guadalupe <github.com/leonidguadalupe>
"""
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Sync
from api.serializers import SyncSerializer

from aquila.settings import (
    LAKE_DB_NAME, LAKE_DB_USER, LAKE_DB_PASSWORD, LAKE_DB_HOST, LAKE_DB_PORT,
    LAKE_MSSQL_DB_NAME, LAKE_MSSQL_DB_USER, LAKE_MSSQL_DB_PASSWORD,
    LAKE_MSSQL_DB_HOST
)

from tools import DatabaseHelper, Mssql, Postgres


class SyncViewSet(viewsets.ViewSet):
    queryset = Sync.objects.all()
    serializer_class = SyncSerializer

    def _get_object(self, id):
        try:
            return Sync.objects.get(id=id)
        except Sync.DoesNotExist:
            raise Http404

    @action(detail=True, url_path='syncs', url_name='syncs', methods=['get'])
    def list(self, request):
        syncs = Sync.objects.all()
        serializer = self.serializer_class(syncs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, url_path='create', url_name='create', methods=['post'])  # noqa:E501
    def create(self, request):
        """
        This is the functionality for syncing
        it records the syncs and will return a success flag if it worked
        TODO: create a celery job instead and return the job ID
        """

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            mssql_obj = {
                'LAKE_MSSQL_DB_NAME': LAKE_MSSQL_DB_NAME,
                'LAKE_MSSQL_DB_USER': LAKE_MSSQL_DB_USER,
                'LAKE_MSSQL_DB_PASSWORD': LAKE_MSSQL_DB_PASSWORD,
                'LAKE_MSSQL_DB_HOST': LAKE_MSSQL_DB_HOST
            }
            psql_obj = {
                'LAKE_DB_NAME': LAKE_DB_NAME,
                'LAKE_DB_USER': LAKE_DB_USER,
                'LAKE_DB_PASSWORD': LAKE_DB_PASSWORD,
                'LAKE_DB_HOST': LAKE_DB_HOST,
                'LAKE_DB_PORT': LAKE_DB_PORT
            }
            # Get connections and cursors using the class helper
            mhelper = DatabaseHelper(mssql=mssql_obj)
            phelper = DatabaseHelper(postgresql=psql_obj)

            # Get external data
            external_db_data = Mssql(mhelper)

            # Use results and sync to postgres
            external_db_data = Postgres(phelper, external_db_data.all_data,
                                        external_db_data.primary_keys_names,
                                        external_db_data.primary_keys
                                        )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        sync = self._get_object(id=pk)
        if pk:
            serializer = self.serializer_class(sync, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

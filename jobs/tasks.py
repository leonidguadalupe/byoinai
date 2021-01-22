from celery import task

from api.models import Sync
from tools import DatabaseHelper, Mssql, Postgres

from aquila.settings import (
    LAKE_DB_NAME, LAKE_DB_USER, LAKE_DB_PASSWORD, LAKE_DB_HOST, LAKE_DB_PORT,
    LAKE_MSSQL_DB_NAME, LAKE_MSSQL_DB_USER, LAKE_MSSQL_DB_PASSWORD,
    LAKE_MSSQL_DB_HOST
)


@task
def sync_external_db():
    sync = Sync.objects.create(status=Sync.REQUESTED)

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
    mhelper = DatabaseHelper(mssql=mssql_obj, sync=sync)
    phelper = DatabaseHelper(postgresql=psql_obj, sync=sync)

    # Get external data
    external_db_data = Mssql(mhelper, sync)

    # Use results and sync to postgres
    external_db_data = Postgres(phelper, external_db_data.all_data,
                                external_db_data.primary_keys_names,
                                external_db_data.primary_keys, sync
                                )
    sync.status = Sync.SUCCESS
    sync.save()

import psycopg2
import pymssql
import socket

from collections import defaultdict
# from aquila.settings import (
#     LAKE_DB_NAME, LAKE_DB_USER, LAKE_DB_PASSWORD,
#     LAKE_MSSQL_DB_NAME, LAKE_MSSQL_DB_USER, LAKE_MSSQL_DB_PASSWORD,
#     LAKE_MSSQL_DB_HOST
# )

class DatabaseMeta(type):
    """
        Metaclass for auto creation of cursors. This will make things more scalable
        as we add more databases to work with.
    """
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)

        if hasattr(obj, 'mssql'):
            try:
                host = obj.mssql['LAKE_MSSQL_DB_HOST']
                database = obj.mssql['LAKE_MSSQL_DB_NAME']
                user = obj.mssql['LAKE_MSSQL_DB_USER']
                password = obj.mssql['LAKE_MSSQL_DB_PASSWORD']

            except KeyError as e:
                raise Exception(e)

            ip = socket.gethostbyname(host)

            obj.mssql_conn = pymssql.connect(
                host=ip,
                password=password,
                database=database,
                user=user
            )
            obj.mssql_cursor = obj.mssql_conn.cursor(as_dict=True)

        if hasattr(obj, 'postgresql'):
            try:
                host = obj.postgresql['LAKE_DB_HOST']
                database = obj.postgresql['LAKE_DB_NAME']
                user = obj.postgresql['LAKE_DB_USER']
                password = obj.postgresql['LAKE_DB_PASSWORD']
            except KeyError as e:
                raise Exception(e)

            obj.postgres_conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(database, user, host, password))
            obj.postgres_cursor = obj.postgres_conn.cursor()

        return obj

class DatabaseHelper(object, metaclass=DatabaseMeta):
    def __init__(self, **kwargs):
        if 'postgresql' in kwargs:
            self.postgresql = kwargs['postgresql']

        if 'mssql' in kwargs:
            self.mssql = kwargs['mssql']



#helper = DatabaseHelper(mssql=mssql_obj, postgresql=psql_obj)
#print('success')
#a = Mssql(helper)
# print(a.tables)
# print(a.table_columns)
# print(a.primary_keys)
#print(a.all_data['departments']['18'])
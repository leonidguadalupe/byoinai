import copy
import psycopg2
from contextlib import contextmanager
from typing import List, Iterable
from collections import defaultdict
from psycopg2 import sql
from psycopg2.extensions import AsIs
class Postgres(object):
    def __init__(self, obj, mssql_data, pknames, pks):
        self.cursor = obj.postgres_cursor
        self.conn = obj.postgres_conn
        self.tables = []
        self.table_columns = {}
        self.primary_keys_names = pknames
        self.primary_keys = pks
        self.all_data = defaultdict(dict)

        if self.conn:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    ## fill in table names
                    self.get_tables(cursor,)

                    ## fill in column names for schema validation.
                    self.get_columns(cursor, self.tables)

                    ## fill in primary keys
                    ## TODO: we are going to look for foreignkeys as well in the future to fill 
                    ## that entity first before the concerned table
                    #self.get_primary_key_column_names(cursor, self.tables)

                    self.all_data = mssql_data
                    self.store_data_db(cursor, conn)

    def get_tables(self, cursor) -> None:
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        result = [row[0] for row in cursor]

        self.tables = result

    def get_columns(self, cursor, tables: list) -> None:
        for table in tables:

            cursor.execute("""
                SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table}'
            """.format(
                table=table
            ))
            columns = [row[0] for row in cursor]
            self.table_columns[table] = columns

    def store_data_db(self, cursor, conn) -> None:
        if self.all_data:
            for table in self.tables:
                columns = copy.deepcopy(self.table_columns[table])
                pk = self.primary_keys_names[table].lower()
                ## unpacking values to dynamically create sql queries through
                ## iterating tables. using composed elements with sql.
                column_str = sql.SQL(', ').join([sql.Identifier(xa) for xa in columns])
                columns.remove(pk)
                column_str_less_pk = sql.SQL(', ').join([sql.Identifier(xa) for xa in columns])
                ## Identifiers are for table names and columns
                ## Excluded does not belong to both
                excl_str = sql.SQL(', ').join([sql.SQL('EXCLUDED.') + sql.Identifier(str(column)) for column in columns])
                

                ## TODO: Will be using copy_from to make this script scalable
                for value in self.all_data[table]:
                    values_list = []
                    for co in self.table_columns[table]:
                        try:
                            temp = value[co]
                        except:
                            ## simple hack since we need to override pymssql as_dict function in cursor to produce
                            ## lowercase keys. 
                            ## best solution would be to retain case of column names during schema migration using pgloader
                            ## so I'm adding that on TODO
                            temp = value[co.upper()]

                        if temp != None:
                            values_list.append(str(temp))
                        else:
                            values_list.append(None)
                    ## adding %s placeholders for the values
                    placeholder = sql.SQL(', ').join(sql.Placeholder() * len(values_list))

                    ## query does an raw upsert in the database
                    insert_sql = sql.SQL("""
                        INSERT INTO {} ({}) VALUES ({}) ON CONFLICT ({}) DO UPDATE SET ({}) = ({})
                    """).format(sql.Identifier(table), column_str, placeholder, sql.Identifier(pk), column_str_less_pk, excl_str)

                    cursor.execute(insert_sql, values_list)

            conn.commit()

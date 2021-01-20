import pymssql
from collections import defaultdict

class Mssql(object):
    def __init__(self, obj):
        self.cursor = obj.mssql_cursor
        self.conn = obj.mssql_conn
        self.tables = []
        self.table_columns = {}
        self.primary_keys_names = {}
        self.primary_keys = defaultdict(list)
        self.all_data = defaultdict(list)

        if self.conn:
            with self.conn as conn:
                with conn.cursor(as_dict=True) as cursor:
                    ## fill in table names
                    self.get_tables(cursor,)

                    ## fill in column names for schema validation.
                    self.get_columns(cursor, self.tables)

                    ## fill in primary keys
                    ## TODO: we are going to look for foreignkeys as well in the future to fill 
                    ## that entity first before the concerned table
                    self.get_primary_key_column_names(cursor, self.tables)

                    ## 
                    self.fetch_and_store_data(cursor, self.tables)

    def get_tables(self, cursor) -> None:
        cursor.execute("""
            select t.name as table_name
            from sys.tables t
        """)

        self.tables = [row['table_name'] for row in cursor]

    def get_columns(self, cursor, tables: list) -> None:
        for table in tables:

            cursor.execute("""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = N'{table}'
            """.format(
                table=table
            ))
            columns = [row['COLUMN_NAME'].lower() for row in cursor if not row['COLUMN_NAME'].startswith('IF_')]
            self.table_columns[table] = columns

    def get_primary_key_column_names(self, cursor, tables) -> None:
        for table in tables:

            cursor.execute("""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE OBJECTPROPERTY(OBJECT_ID(CONSTRAINT_SCHEMA + '.' + QUOTENAME(CONSTRAINT_NAME)), 'IsPrimaryKey') = 1
                AND TABLE_NAME = '{table}'
            """.format(
                table=table
            ))
            try:
                self.primary_keys_names[table] = cursor.fetchone()['COLUMN_NAME']
            except KeyError as e:
                raise Exception('Failed to initialize primary keys. Missing key: {}'.format(e))

    def fetch_and_store_data(self, cursor, tables) -> None:
        for table in tables:
            pk = self.primary_keys_names[table]
            cursor.execute("""
                SELECT *
                FROM {table}
            """.format(
                table=table
            ))
            for row in cursor:
                self.all_data[table].append(row)
                ## instead of looping through the keys later, better to consume a bit memory to store these.
                ## will be used for cross checking deleted rows in external db.
                self.primary_keys[table].append(row[pk])
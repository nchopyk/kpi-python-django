import psycopg2
from ..Server import db_tools



class PostgresDb:
    def __init__(self):
        self.connection = psycopg2.connect(
            database="postgres",
            user="admin",
            password="admin",
            host="127.0.0.1",
            port="5432",
        )
        self.cursor = self.connection.cursor()
        print("PostgreSQL: connection successful")

        self._create_technique_table()
        self._create_specifications_table()
        self._create_prices_table()

    def import_records(self, columns, records):
        for row in records:
            print("PostgreSQL: beginning transaction")
            try:
                sql_add_technique = db_tools.generate_technique_insert_row_sql(columns, row)
                sql_add_specifications_to_technique = db_tools.generate_specifications_insert_row_sql(columns, row)
                sql_add_prices_to_technique = db_tools.generate_prices_insert_row_sql(columns, row)

                self.cursor.execute(sql_add_technique)
                self.cursor.execute(sql_add_specifications_to_technique)
                self.cursor.execute(sql_add_prices_to_technique)

                self.connection.commit()

                print('PostgreSQL: row was successfully exported to Postgres')
            except psycopg2.DatabaseError:
                print("PostgreSQL: transaction failed, rollback")

        print('PostgreSQL: records were successfully exported to Postgres')

    def get_all_records(self):
        sql_get_all_records = """   SELECT technique.id, technique.name, technique.brand, specifications.size,
                                    specifications.energy_efficiency_class, prices.electricity_costs_per_year, prices.price
                                    FROM technique
                                    INNER JOIN specifications ON technique.id = specifications.technique_id 
                                    INNER JOIN prices ON technique.id = prices.technique_id """

        self.cursor.execute(sql_get_all_records)
        records = self.cursor.fetchall()
        return records

    def close(self):
        self.connection.close()

    def _create_technique_table(self):
        sql_create_technique_table = """CREATE TABLE IF NOT EXISTS technique (id INTEGER PRIMARY KEY, name TEXT, brand TEXT);"""
        self.cursor.execute(sql_create_technique_table)
        self.connection.commit()
        print("PostgreSQL: technique table created (or already exists)")

    def _create_specifications_table(self):
        sql_create_specifications_table = """CREATE TABLE IF NOT EXISTS specifications (
                                             id INTEGER PRIMARY KEY,
                                             size TEXT, 
                                             energy_efficiency_class TEXT,
                                             technique_id INTEGER ,
                                             FOREIGN KEY(technique_id) REFERENCES technique(id) ON DELETE CASCADE);"""
        self.cursor.execute(sql_create_specifications_table)
        self.connection.commit()
        print("PostgreSQL: specifications table created (or already exists)")

    def _create_prices_table(self):
        sql_create_prices_table = """CREATE TABLE IF NOT EXISTS prices (
                                     id INTEGER PRIMARY KEY,
                                     price INTEGER,
                                     electricity_costs_per_year TEXT,
                                     technique_id INTEGER ,
                                     FOREIGN KEY(technique_id) REFERENCES technique(id) ON DELETE CASCADE); """
        self.cursor.execute(sql_create_prices_table)
        self.connection.commit()
        print("PostgreSQL: prices table created (or already exists)")

import mysql.connector

from ..Server import db_tools


class MysqlDb:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="mysql"
        )
        self.cursor = self.connection.cursor()
        print("MySQL: connection successful")

        self._create_technique_table()
        self._create_specifications_table()
        self._create_prices_table()

    def import_record(self, columns, records):
        print("MySQL: beginning transaction")
        last_row = records[-1]

        try:
            sql_add_technique = db_tools.generate_technique_insert_row_sql(columns, last_row, syntax='mysql')
            sql_add_specifications_to_technique = db_tools.generate_specifications_insert_row_sql(columns, last_row, syntax='mysql')
            sql_add_prices_to_technique = db_tools.generate_prices_insert_row_sql(columns, last_row, syntax='mysql')

            self.cursor.execute(sql_add_technique)
            self.cursor.execute(sql_add_specifications_to_technique)
            self.cursor.execute(sql_add_prices_to_technique)

            self.connection.commit()

            print('MySQL: row was successfully exported to MySQL')
        except mysql.connector.Error:
            print("Mysql: transaction failed, rollback")

    def get_all_records(self):
        sql_get_all_records = """   SELECT technique.id, technique.name, technique.brand, specifications.size,
                                    specifications.energy_efficiency_class, prices.electricity_costs_per_year, prices.price
                                    FROM technique
                                    INNER JOIN specifications ON technique.id = specifications.technique_id 
                                    INNER JOIN prices ON technique.id = prices.technique_id """

        self.cursor.execute(sql_get_all_records)
        records = self._remove_none_from_records(self.cursor.fetchall())
        return records

    def close(self):
        self.connection.close()

    def _create_technique_table(self):
        sql_create_technique_table = """CREATE TABLE IF NOT EXISTS technique (id INTEGER PRIMARY KEY, name TEXT, brand TEXT);"""
        self.cursor.execute(sql_create_technique_table)
        self.connection.commit()
        print("MySQL: technique table created (or already exists)")

    def _create_specifications_table(self):
        sql_create_specifications_table = """CREATE TABLE IF NOT EXISTS specifications (
                                             id INTEGER PRIMARY KEY,
                                             size TEXT, 
                                             energy_efficiency_class TEXT,
                                             technique_id INTEGER ,
                                             FOREIGN KEY(technique_id) REFERENCES technique(id) ON DELETE CASCADE);"""
        self.cursor.execute(sql_create_specifications_table)
        self.connection.commit()
        print("MySQL: specifications table created (or already exists)")

    def _create_prices_table(self):
        sql_create_prices_table = """CREATE TABLE IF NOT EXISTS prices (
                                     id INTEGER PRIMARY KEY,
                                     price TEXT,
                                     electricity_costs_per_year TEXT,
                                     technique_id INTEGER ,
                                     FOREIGN KEY(technique_id) REFERENCES technique(id) ON DELETE CASCADE); """
        self.cursor.execute(sql_create_prices_table)
        self.connection.commit()
        print("MySQL: prices table created (or already exists)")

    def _remove_none_from_records(self, records):
        records_to_return = []
        for record in records:
            row_to_return = []
            for column in record:
                if column is not None:
                    row_to_return.append(column)
            records_to_return.append(tuple(row_to_return))

        return records_to_return

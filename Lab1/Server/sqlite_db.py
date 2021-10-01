import sqlite3


class DateBase:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()
        print("SQLite: connection successful")

        self._create_technique_table()
        self._create_specifications_table()
        self._create_prices_table()

    def add_technique(self, name, brand, size, energy_efficiency_class, electricity_costs_per_year, price):
        sql_add_technique = """INSERT  INTO technique (name, brand) VALUES (?, ?)"""
        sql_add_specifications_to_technique = """INSERT  INTO specifications (size, energy_efficiency_class, technique_id) VALUES (?, ?, ?)"""
        sql_add_prices_to_technique = """INSERT  INTO prices (price, electricity_costs_per_year, technique_id) VALUES (?, ?, ?)"""

        print("SQLite: beginning transaction")
        self.cursor.execute("BEGIN TRANSACTION")
        try:
            self.cursor.execute(sql_add_technique, (name, brand))
            technique_id = self.cursor.lastrowid
            self.cursor.execute(sql_add_specifications_to_technique, (size, energy_efficiency_class, technique_id))
            self.cursor.execute(sql_add_prices_to_technique, (price, electricity_costs_per_year, technique_id))
            self.connection.commit()
            print("SQLite: record successfully inserted")
        except self.connection.Error:
            self.cursor.execute("rollback")
            print("SQLite: transaction failed, rollback")

    def edit_technique(self, id, name, brand, size, energy_efficiency_class, electricity_costs_per_year, price):
        sql_update_technique = """UPDATE technique SET name = ?, brand = ?  WHERE id = ?;"""
        sql_update_specifications_to_technique = """UPDATE specifications SET size = ?, energy_efficiency_class = ?  WHERE technique_id = ?;"""
        sql_update_prices_to_technique = """UPDATE prices SET price = ?, electricity_costs_per_year = ?  WHERE technique_id = ?;"""

        print("SQLite: beginning transaction")
        self.cursor.execute("BEGIN TRANSACTION")
        try:
            self.cursor.execute(sql_update_technique, (name, brand, id))
            self.cursor.execute(sql_update_specifications_to_technique, (size, energy_efficiency_class, id))
            self.cursor.execute(sql_update_prices_to_technique, (price, electricity_costs_per_year, id))
            self.connection.commit()
            print("SQLite: record successfully updated")
        except self.connection.Error:
            self.cursor.execute("rollback")
            print("SQLite: transaction failed, rollback")
            print(self.connection.Error)

    def get_all_technique(self):
        sql_get_all_technique = """ SELECT technique.id, technique.name, technique.brand, specifications.size, 
                                    specifications.energy_efficiency_class, prices.electricity_costs_per_year, prices.price
                                    FROM technique
                                    INNER JOIN specifications ON technique.id = specifications.technique_id 
                                    INNER JOIN prices ON technique.id = prices.technique_id """

        self.cursor.execute(sql_get_all_technique)
        records = self.cursor.fetchall()
        return records

    def delete_technique_by_id(self, id):
        sql_delete_technique = """DELETE FROM technique WHERE id = ?;"""

        self.cursor.execute(sql_delete_technique, (id,))
        self.connection.commit()
        print("SQLite: record successfully deleted")

    def close(self):
        self.connection.close()

    def _create_technique_table(self):
        sql_create_technique_table = """CREATE TABLE IF NOT EXISTS technique (id INTEGER PRIMARY KEY, name TEXT NOT NULL, brand TEXT);"""
        self.cursor.execute(sql_create_technique_table)
        self.connection.commit()
        print("SQLite: technique table created (or already exists)")

    def _create_specifications_table(self):
        sql_create_specifications_table = """CREATE TABLE IF NOT EXISTS specifications (
                                             id INTEGER PRIMARY KEY,
                                             size TEXT, 
                                             energy_efficiency_class TEXT,
                                             technique_id INTEGER ,
                                             FOREIGN KEY(technique_id) REFERENCES technique(id) ON DELETE CASCADE);"""
        self.cursor.execute(sql_create_specifications_table)
        self.connection.commit()
        print("SQLite: specifications table created (or already exists)")

    def _create_prices_table(self):
        sql_create_prices_table = """CREATE TABLE IF NOT EXISTS prices (
                                     id INTEGER PRIMARY KEY,
                                     price INTEGER NOT NULL,
                                     electricity_costs_per_year TEXT,
                                     technique_id INTEGER ,
                                     FOREIGN KEY(technique_id) REFERENCES technique(id) ON DELETE CASCADE); """
        self.cursor.execute(sql_create_prices_table)
        self.connection.commit()
        print("SQLite: prices table created (or already exists)")


db = DateBase('sqlite.db')
# db.add_technique("TV", "Samsung", "1", "A+1", "1", "1")
db.add_technique("TV2", "Samsung2", "2", "A+2", "2", "price")
# db.edit_technique(3, "TV", "LG", "77777777", "7777777", "777777777", "777777")
for row in db.get_all_technique():
    print(row)

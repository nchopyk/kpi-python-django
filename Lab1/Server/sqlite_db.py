import sqlite3


class DateBase:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        sql_create_consumer_electronics_table = """ CREATE TABLE IF NOT EXISTS consumer_electronics (
                                                    id integer PRIMARY KEY,
                                                    name TEXT NOT NULL,
                                                    brand TEXT NOT NULL,
                                                    size TEXT,
                                                    energy_efficiency_class TEXT,
                                                    electricity_costs_per_year TEXT,
                                                    price INTEGER NOT NULL); """

        self.cursor.execute(sql_create_consumer_electronics_table)
        self.connection.commit()

    def add_technique(self, name, brand, size, energy_efficiency_class, electricity_costs_per_year, price):
        sql_add_technique = """ INSERT  INTO consumer_electronics (name, brand, size, energy_efficiency_class, electricity_costs_per_year, price) 
                                VALUES ( ?,?,?,?,?,? ) """
        fields = (name, brand, size, energy_efficiency_class, electricity_costs_per_year, price)

        self.cursor.execute(sql_add_technique, fields)
        self.connection.commit()

    def edit_technique(self, id, name, brand, size, energy_efficiency_class, electricity_costs_per_year, price):
        sql_edit_technique = """UPDATE consumer_electronics
                                SET name = ?, brand = ?, size = ?, energy_efficiency_class = ?, electricity_costs_per_year = ?, price = ? 
                                WHERE id = ?;"""
        fields = (name, brand, size, energy_efficiency_class, electricity_costs_per_year, price, id)

        self.cursor.execute(sql_edit_technique, fields)
        self.connection.commit()

    def delete_technique_by_id(self, id):
        sql_delete_technique = """DELETE FROM consumer_electronics WHERE id = ?;"""

        self.cursor.execute(sql_delete_technique, (id,))
        self.connection.commit()

    def get_all_technique(self, sort_by=None, order="ASC"):

        if sort_by:
            print("Sort")
            sql_get_all_technique = """SELECT * FROM consumer_electronics ORDER BY """ + sort_by + " " + order
            self.cursor.execute(sql_get_all_technique)
        else:
            print("No sort")
            sql_get_all_technique = """SELECT * FROM consumer_electronics"""
            self.cursor.execute(sql_get_all_technique)

        records = self.cursor.fetchall()
        return records

    def close(self):
        self.connection.close()

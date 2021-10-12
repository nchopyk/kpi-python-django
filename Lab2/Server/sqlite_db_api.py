from peewee import *
from Lab2.Server.postgress_db_api import PostgresApi
from Lab2.Server.mysql_db_api import MySQLApi
sqlite_db = SqliteDatabase('sqlite.db')

class Technique(Model):
    id = PrimaryKeyField(unique=True)
    name = CharField()
    brand = CharField()

    class Meta:
        database = sqlite_db


class Specification(Model):
    size = CharField()
    energy_efficiency_class = CharField()
    technique = ForeignKeyField(Technique, backref='specifications')

    class Meta:
        database = sqlite_db


class Price(Model):
    price = IntegerField()
    electricity_costs_per_year = IntegerField()
    technique = ForeignKeyField(Technique, backref='prices')

    class Meta:
        database = sqlite_db


class SQLiteApi():
    def __init__(self):
        sqlite_db.connect()
        sqlite_db.create_tables([Technique, Specification, Price])

    def add_technique(self, name, brand, size, energy_efficiency_class, price, electricity_costs_per_year):
        technique = Technique.create(name=name, brand=brand)
        specifications = Specification.create(size=size, energy_efficiency_class=energy_efficiency_class, technique=technique)
        price = Price.create(price=price, electricity_costs_per_year=electricity_costs_per_year, technique=technique)

    def edit_technique(self, id, name, brand, size, energy_efficiency_class, price, electricity_costs_per_year):
        technique = Technique.update(name=name, brand=brand).where(Technique.id==id)
        specifications = Specification.update(size=size, energy_efficiency_class=energy_efficiency_class).where(Specification.technique == id)
        prices = Price.update(price=price, electricity_costs_per_year=electricity_costs_per_year).where(Price.technique == id)

        technique.execute()
        specifications.execute()
        prices.execute()

    def delete_technique_by_id(self, id):
        technique = Technique.delete().where(Technique.id==id)
        specifications = Specification.delete().where(Specification.technique == id)
        prices = Price.delete().where(Price.technique == id)

        technique.execute()
        specifications.execute()
        prices.execute()

    def get_all_records(self):
        query = (Technique
                 .select(Technique.id,
                         Technique.name,
                         Technique.brand,
                         Specification.size,
                         Specification.energy_efficiency_class,
                         Price.price,
                         Price.electricity_costs_per_year)
                 .join(Price, on=(Technique.id == Price.technique))
                 .join(Specification, on=(Technique.id == Specification.technique)))
        return list(query.dicts())

    def export_to_database2(self):
        records = self.get_all_records()
        postgres = PostgresApi()
        postgres.import_records(records)

    def export_to_database3(self):
        records = self.get_all_records()
        mysql = MySQLApi()
        if records:
            mysql.import_record(records[0])





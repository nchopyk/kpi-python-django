from peewee import *

psql_db = PostgresqlDatabase(
    'postgres',
    user='admin',
    password='admin',
    host='127.0.0.1',
    port='5433')


class Technique(Model):
    name = CharField()
    brand = CharField()

    class Meta:
        database = psql_db


class Specification(Model):
    size = CharField()
    energy_efficiency_class = CharField()
    technique = ForeignKeyField(Technique, backref='specifications')

    class Meta:
        database = psql_db


class Price(Model):
    price = IntegerField()
    electricity_costs_per_year = IntegerField()
    technique = ForeignKeyField(Technique, backref='prices')

    class Meta:
        database = psql_db


class PostgresApi():
    def __init__(self):
        psql_db.connect()
        psql_db.create_tables([Technique, Specification, Price])

    def crate_technique(self, name, brand, size, energy_efficiency_class, price, electricity_costs_per_year):
        technique = Technique.create(name=name, brand=brand)
        specifications = Specification.create(size=size, energy_efficiency_class=energy_efficiency_class, technique=technique)
        price = Price.create(price=price, electricity_costs_per_year=electricity_costs_per_year, technique=technique)

        technique.save()
        specifications.save()
        price.save()

    def get_all_records(self):
        query = (Technique
                 .select(Technique.name,
                         Technique.brand,
                         Specification.size,
                         Specification.energy_efficiency_class,
                         Price.price,
                         Price.electricity_costs_per_year)
                 .join(Price, on=(Technique.id == Price.technique))
                 .join(Specification, on=(Technique.id == Specification.technique)))
        return list(query.dicts())


db = PostgresApi()
db.crate_technique("SMarrtPhoen", "Samsung", "12", "A+", 12, 12)
for row in db.get_all_records():
    print(row)

print(db.get_all_records())

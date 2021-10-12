from peewee import *

mysql_db = MySQLDatabase('mysql', user='root', password='admin',
                         host='localhost', port=3307)


class Technique(Model):
    name = CharField()
    brand = CharField()

    class Meta:
        database = mysql_db


class Specification(Model):
    energy_efficiency_class = CharField()
    technique = ForeignKeyField(Technique, backref='specifications')

    class Meta:
        database = mysql_db


class Price(Model):
    price = IntegerField()
    technique = ForeignKeyField(Technique, backref='prices')

    class Meta:
        database = mysql_db


class MySQLApi():
    def __init__(self):
        mysql_db.create_tables([Technique, Specification, Price])

    def create_technique(self, name, brand, energy_efficiency_class, price):
        technique = Technique.create(name=name, brand=brand)
        specifications = Specification.create(energy_efficiency_class=energy_efficiency_class, technique=technique)
        price = Price.create(price=price, technique=technique)

    def get_all_records(self):
        query = (Technique
                 .select(Technique.id,
                         Technique.name,
                         Technique.brand,
                         Specification.energy_efficiency_class,
                         Price.price)
                 .join(Price, on=(Technique.id == Price.technique))
                 .join(Specification, on=(Technique.id == Specification.technique)))
        return list(query.dicts())

    def import_record(self, record):
        self.create_technique(record["name"], record["brand"], record["energy_efficiency_class"], record["price"])


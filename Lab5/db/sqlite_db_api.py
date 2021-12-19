from peewee import *

sqlite_db = SqliteDatabase('./db/sqlite.db')


class BaseModel(Model):
    class Meta:
        database = sqlite_db


class Technique(BaseModel):
    id = PrimaryKeyField(unique=True)
    model = CharField()
    brand = CharField()

    energy_efficiency_class = CharField()
    size = CharField()

    electricity_costs_per_year = IntegerField()
    price = IntegerField()


class Photos(BaseModel):
    id = PrimaryKeyField(unique=True)
    path = CharField()
    technique_id = ForeignKeyField(Technique.id, backref='photos')


class DatabaseClient:
    def __init__(self):
        sqlite_db.connect()
        sqlite_db.create_tables([Technique, Photos])

    def add_technique(self, model, brand, size, energy_efficiency_class, price, electricity_costs_per_year, photo_path):
        technique = Technique.create(model=model, brand=brand,
                                     size=size, energy_efficiency_class=energy_efficiency_class,
                                     price=price, electricity_costs_per_year=electricity_costs_per_year)
        Photos.create(path=photo_path, technique_id=technique)

    def edit_technique(self, id, model, brand, size, energy_efficiency_class, price, electricity_costs_per_year, photo_path):
        technique = Technique.update(model=model, brand=brand,
                                     size=size, energy_efficiency_class=energy_efficiency_class,
                                     price=price, electricity_costs_per_year=electricity_costs_per_year
                                     ).where(Technique.id == id)
        photo = Photos.update(path=photo_path, technique_id=technique).where(Photos.technique_id == id)

        technique.execute()
        photo.execute()

    def delete_technique_by_id(self, id):
        technique = Technique.delete().where(Technique.id == id)
        specifications = Photos.delete().where(Photos.technique_id == id)

        technique.execute()
        specifications.execute()

    def get_all_technique(self):
        query = (Technique
                 .select(Technique.id,
                         Technique.model,
                         Technique.brand,
                         Technique.size,
                         Technique.energy_efficiency_class,
                         Technique.price,
                         Technique.electricity_costs_per_year,
                         Photos.path.alias('photo_local_url'))
                 .join(Photos, on=(Technique.id == Photos.technique_id)))
        return list(query.dicts())

    def get_technique_by_id(self, id):
        query = (Technique
                 .select(Technique.id,
                         Technique.model,
                         Technique.brand,
                         Technique.size,
                         Technique.energy_efficiency_class,
                         Technique.price,
                         Technique.electricity_costs_per_year,
                         Photos.path.alias('photo_local_url'))
                 .join(Photos, on=(Technique.id == Photos.technique_id))
                 .where(Technique.id == id))
        return list(query.dicts())[0]

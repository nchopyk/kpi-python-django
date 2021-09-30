import psycopg2


class PostgresDb:
    def __init__(self):
        self.connection = psycopg2.connect(
            database="postgres",
            user="admin",
            password="admin",
            host="127.0.0.1",
            port="5432",
        )
        print("PostgreSQL: connection successful")

        self.cursor = self.connection.cursor()
        self.create_electronics_table()

    def create_electronics_table(self):
        sql_create_consumer_electronics_table = """ CREATE TABLE IF NOT EXISTS consumer_electronics (
                                                    id integer PRIMARY KEY,
                                                    name TEXT,
                                                    brand TEXT,
                                                    size TEXT,
                                                    energy_efficiency_class TEXT,
                                                    electricity_costs_per_year TEXT,
                                                    price INTEGER); """

        self.cursor.execute(sql_create_consumer_electronics_table)
        self.connection.commit()
        print("PostgreSQL: electronics table created")

    def import_records(self, columns, records):
        rows_to_insert = self._remove_unnecessary_columns(columns, records)
        sql_bulk_insert = f"INSERT INTO consumer_electronics ({', '.join(columns)}) VALUES {', '.join(rows_to_insert)} ON CONFLICT (id) {self._on_conflict_do_update(columns)}"

        self.cursor.execute(sql_bulk_insert)
        self.connection.commit()
        print('PostgreSQL: records successfully exported to Postgres')

    def get_all_records(self):
        sql_get_all_records = """SELECT * FROM consumer_electronics"""

        self.cursor.execute(sql_get_all_records)
        records = self._remove_none_from_records(self.cursor.fetchall())
        return records

    def close(self):
        self.connection.close()

    def _remove_unnecessary_columns(self, columns_to_keep, records):
        all_columns = ('id', 'name', 'brand', 'size', 'energy_efficiency_class', 'electricity_costs_per_year', 'price')
        rows_to_insert = []

        for row in records:
            row_to_insert = []
            if "id" not in columns_to_keep: columns_to_keep.insert(0, 'id')

            for column in columns_to_keep:
                row_to_insert.append(row[all_columns.index(column)])
            rows_to_insert.append(str(tuple(row_to_insert)))

        return rows_to_insert

    def _on_conflict_do_update(self, columns):
        if "id" in columns:
            columns.remove("id")

        fields = []
        for column in columns:
            fields.append(f"{column}=EXCLUDED.{column}")

        return f"DO UPDATE SET {', '.join(fields)}"

    def _remove_none_from_records(self, records):
        records_to_return = []
        for record in records:
            row_to_return = []
            for column in record:
                if column is not None:
                    row_to_return.append(column)
            records_to_return.append(tuple(row_to_return))

        return records_to_return


db = PostgresDb()
test_records = [(1, 'Wicroowave CHANGED2', 'Test', 'Lardge', 'V6+', '8888', 8888), (3, 'Qicroowave', 'Test', 'Lardge', 'V6+', '8888', 8888),
                (4, 'Bicroowwwwwwwave', 'Test', 'Lardge', 'V6+', '8888', 8888), (5, 'Microowave', 'Lanos', 'Lardge', 'V6+', '8888', 8888)]
db.import_records(['name', 'brand', 'size'], test_records)  # id already included
print(db.get_all_records())

def remove_unnecessary_columns(columns_to_keep, row, skip_id=False):
    all_columns = ("id", 'name', 'brand', 'size', 'energy_efficiency_class', 'electricity_costs_per_year', 'price')

    columns_to_keep = list(columns_to_keep)
    if "id" not in columns_to_keep and not skip_id: columns_to_keep.insert(0, "id")

    row_to_insert = []
    for column in columns_to_keep:
        row_to_insert.append(row[all_columns.index(column)])

    return row_to_insert


def on_conflict_do_update(columns, syntax='postgres'):
    fields = []
    if syntax == 'postgres':
        for column in columns:
            fields.append(f"{column}=EXCLUDED.{column}")
        return f"ON CONFLICT (id) DO UPDATE SET {', '.join(fields)}"
    elif syntax == 'mysql':
        for column in columns:
            fields.append(f"{column}={column}")
        return f"ON DUPLICATE KEY UPDATE {', '.join(fields)}"
    else:
        return ""


def generate_technique_insert_row_sql(columns_to_keep, row, syntax="postgres"):
    all_technique_columns = ['id', 'name', 'brand']
    technique_columns_to_keep = [column for column in all_technique_columns if column in columns_to_keep or column == "id"]
    technique_row_to_insert = remove_unnecessary_columns(technique_columns_to_keep, row)

    if syntax == 'postgres':
        sql = f"INSERT INTO technique ({', '.join(technique_columns_to_keep)}) VALUES {tuple(technique_row_to_insert)} " \
              f"{on_conflict_do_update(technique_columns_to_keep, syntax='postgres')};"
    elif syntax == "mysql":
        sql = f"INSERT INTO technique ({', '.join(technique_columns_to_keep)}) VALUES {tuple(technique_row_to_insert)} " \
              f"{on_conflict_do_update(technique_columns_to_keep, syntax='mysql')};"
    else:
        sql = f"INSERT INTO technique ({', '.join(technique_columns_to_keep)}) VALUES {tuple(technique_row_to_insert)};"

    return sql


def generate_specifications_insert_row_sql(columns_to_keep, row, syntax='postgres'):
    all_specifications_columns = ['id', 'size', 'energy_efficiency_class', 'technique_id']
    specifications_columns_to_keep = [column for column in all_specifications_columns if column in columns_to_keep or column == "id"]
    specifications_row_to_insert = remove_unnecessary_columns(specifications_columns_to_keep, row)
    specifications_row_to_insert.append(row[0])

    if syntax == 'postgres':
        sql = f"INSERT INTO specifications ({', '.join(specifications_columns_to_keep)}, technique_id) VALUES {tuple(specifications_row_to_insert)} " \
              f"{on_conflict_do_update(specifications_columns_to_keep, syntax='postgres')};"
    elif syntax == "mysql":
        sql = f"INSERT INTO specifications ({', '.join(specifications_columns_to_keep)}, technique_id) VALUES {tuple(specifications_row_to_insert)} " \
              f"{on_conflict_do_update(specifications_columns_to_keep, syntax='mysql')};"
    else:
        sql = f"INSERT INTO specifications ({', '.join(specifications_columns_to_keep)}, technique_id) VALUES {tuple(specifications_row_to_insert)};"

    return sql


def generate_prices_insert_row_sql(columns_to_keep, row, syntax='postgres'):
    all_prices_columns = ['id', 'electricity_costs_per_year', 'price']
    prices_columns_to_keep = [column for column in all_prices_columns if column in columns_to_keep or column == "id"]
    prices_row_to_insert = remove_unnecessary_columns(prices_columns_to_keep, row)
    prices_row_to_insert.append(row[0])

    if syntax == 'postgres':
        sql = f"INSERT INTO specifications ({', '.join(prices_columns_to_keep)}, technique_id) VALUES {tuple(prices_row_to_insert)} " \
              f"{on_conflict_do_update(prices_columns_to_keep, syntax='postgres')};"
    elif syntax == "mysql":
        sql = f"INSERT INTO specifications ({', '.join(prices_columns_to_keep)}, technique_id) VALUES {tuple(prices_row_to_insert)} " \
              f"{on_conflict_do_update(prices_columns_to_keep, syntax='mysql')};"
    else:
        sql = f"INSERT INTO specifications ({', '.join(prices_columns_to_keep)}, technique_id) VALUES {tuple(prices_row_to_insert)};"

    return sql

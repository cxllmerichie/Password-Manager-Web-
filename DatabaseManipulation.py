from enum import Enum


class DataType(Enum):
    String = 'TEXT'
    Integer = 'INTEGER'
    Float = 'REAL'
    Object = 'BLOB'


class Null(Enum):
    Yes = ''
    No = ' NOT NULL'


class Constraint(Enum):
    Primary = {'abr': 'PK_', 'val': 'PRIMARY KEY'}
    Foreign = {'abr': 'FK_', 'val': 'FOREIGN KEY'}


def create_table(table: str, reference: str = None, constraint: Constraint = None) -> str:
    return f"""
    CREATE TABLE {table.capitalize()} (
        {table.capitalize()}ID integer PRIMARY KEY,
        {constraint.value['val']} (parent_id) REFERENCES parent(id)
        {add_constraint(table, reference, constraint)}
    );
    """


def add_column(table: str, column: str, datatype: DataType, null: Null) -> str:
    return f"""
    ALTER TABLE {table.capitalize()} ADD {column.capitalize()} {datatype.value}{null.value};
    """


def add_constraint(table: str, reference: str, constraint: Constraint) -> str:
    return f"""
    ALTER TABLE {table.capitalize()} ADD {constraint.value['abr']}{reference.capitalize()} {constraint.value['val']} ({reference.capitalize()}_ID) REFERENCES {reference.capitalize()}({reference.capitalize()}ID);
    """


def drop_table(table: str):
    return f"""DROP TABLE {table};"""


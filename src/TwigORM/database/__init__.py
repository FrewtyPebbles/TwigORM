from __future__ import annotations

import sqlite3
from typing import Dict, List
from .statement import Select, Statement, Insert, Update, Delete
from . import statement

class Column:
    def __init__(self, name:str, type:str, constraints:List[str]) -> None:
        self.name = name
        self.constraints = constraints
        self.type = type
    
    def __repr__(self) -> str:
        return f"""{self.name} {self.type} {" ".join(self.constraints)}"""

class Table:
    def __init__(self, database:Database, table_name:str, columns:List[Column]) -> None:
        self.database = database
        self.table_name = table_name
        self.columns = columns
        columns_str = ""
        for cn, col in enumerate(columns):
            if cn == len(columns)-1:
                columns_str += f"{col}"
            else:
                columns_str += f"{col}, "
        createSQL = f"CREATE TABLE IF NOT EXISTS {table_name}({columns_str});"
        database.connection.execute(createSQL)
    
    def select(self, modifier = "", parameters: List[str | Statement | tuple] = ["*"]) -> Select:
        return Select(self, modifier, parameters)

    def insert(self, modifier = "", columns:List[str] = [], parameters: List[str | Statement | tuple] = [], alias = "") -> Select:
        return Insert(self, modifier, columns, parameters, alias)

    def update(self, modifier:str = "", updates:Dict[str, str | int | bool | Statement] = {}, alias = "") -> Select:
        return Update(self, modifier, updates, alias)
    
    def delete(self):
        return Delete(self)

    def drop(self):
        SQL = f"DROP TABLE IF EXISTS {self.table_name}"
        self.database.connection.execute(SQL)


class Database:
    def __init__(self, db_type:str, db_address:str) -> None:
        if db_type.lower() == "sqlite3":
            self.connection = sqlite3.connect(db_address)
            self.db_type = db_type
        self.tables:Dict[str, Table] = {}

    def add_table(self, table_name:str, columns:List[Column]):
        self.tables[table_name] = Table(self, table_name, columns)
        return self

    def close(self):
        self.connection.close()
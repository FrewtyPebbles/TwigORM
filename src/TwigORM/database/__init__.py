from __future__ import annotations

import mysql.connector
import sqlite3
from typing import Dict, List
from .statement import Select, Statement, Insert, Update, Delete
from . import statement

class SQLType:
    Char = "char"
    varchar = "varchar"
    binary = "binary"
    varbinary = "varbinary"
    tinyblob = "tinyblob"
    tinytext = "tinytext"
    text = "text"
    blob = "blob"
    mediumtext = "mediumtext"
    mediumblob = "mediumblob"
    longtext = "longtext"
    longblob = "longblob"
    enum = "enum"
    set = "set"
    bit = "bit"
    tinyint = "tinyint"
    bool = "bool"
    boolean = "bool"
    smallint = "smallint"
    mediumint = "mediumint"
    Int = "int"
    integer = "integer"
    bigint = "bigint"
    float = "float"
    double = "double"
    double_precision = "double precision"
    decimal = "decimal"
    dec = "dec"
    date = "date"
    datetime = "datetime"
    timestamp = "timestamp"
    time = "time"
    year = "year"
    

class ColumnType:
    def __init__(self, sqltype:SQLType | str, *args:str) -> None:
        self.db_type = "sqlite"
        self.type = sqltype
        self.args = args
        self.db_type = "sqlite"

    def render(self):
        # Change column parameter based on db_type
        return f"""{self.type}{f"({', '.join(self.args)})" if len(self.args) != 0 else ""}"""


class Column:
    def __init__(self, type:ColumnType, constraints:List[str]) -> None:
        self.name = ""
        self.constraints = constraints
        self.db_type = "sqlite"
        self.type = type
    
    def __repr__(self) -> str:
        self.type.db_type = self.db_type
        return f"""{self.name} {self.type.render()} {" ".join(self.constraints)}"""

class Table:
    def __init__(self, database:Database, table_name:str, columns:Dict[str, Column]) -> None:
        self.database = database
        self.table_name = table_name
        self.columns = columns
        columns_str = ""
        for cn, (_, col) in enumerate(columns.items()):
            col.db_type = database.db_type
            if cn == len(columns)-1:
                columns_str += f"{col}"
            else:
                columns_str += f"{col}, "
        createSQL = f"CREATE TABLE IF NOT EXISTS {table_name}({columns_str});"
        curs = database.connection.cursor()
        curs.execute(createSQL)
        curs.close()
        database.connection.commit()
        
    
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
        if self.database.db_type == "sqlite":
            self.database.connection.execute(SQL)
        elif self.database.db_type == "mysql":
            curs = self.database.connection.cursor()
            curs.execute(SQL)
            curs.close()
            self.database.connection.commit()


class Database:
    def __init__(self, db_type:str, db_address:str, user = "", password = "", database_name = "") -> None:
        if db_type.lower() == "sqlite":
            self.connection = sqlite3.connect(db_address)
            
        elif db_type.lower() == "mysql":
            params = {}
            if user != "":
                params['user'] = user
            if password != "":
                params['password'] = password
            if database_name != "":
                params['database'] = database_name

            params['host'] = db_address
            
            self.connection = mysql.connector.connect(**params)
            
        self.db_type = db_type
        self.tables:Dict[str, Table] = {}

    def create_database(self, database_name:str):
        if self.db_type == "sqlite":
            print("Error: SQLite3 does not have a CREATE DATABASE functionality.")
            return
        curs = self.connection.cursor()
        sql = f"CREATE DATABASE IF NOT EXISTS {database_name}"
        curs.execute(sql)
        curs.close()
        self.connection.commit()

    def add_table(self, table_name:str, **columns:Column):
        for key in columns.keys():
            columns[key].name = key
        self.tables[table_name] = Table(self, table_name, columns)
        return self

    def close(self):
        self.connection.close()
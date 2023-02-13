from unittest import TestCase
from src.TwigORM.database import ColumnType, Database, Column, SQLType
from src.TwigORM.database.statement.comparison import Equal

dbname = "mysql"

class Testing(TestCase):

    def test_drop(self):
        db = Database(dbname, "127.0.0.1", "testing", "testing", "ORMDatabase")
        db.add_table("Users",
            id = Column(ColumnType(SQLType.Int), ["primary key", "not null", "AUTO_INCREMENT"]),
            Username = Column(ColumnType(SQLType.varchar, "30"), ["not null"]),
            Password = Column(ColumnType(SQLType.varchar, "64"), ["not null"])
        )
        db.tables["Users"].drop()
        db.close()

    def test_createtable(self):
        db = Database(dbname, "127.0.0.1", "testing", "testing", "ORMDatabase")
        db.add_table("Users",
            id = Column(ColumnType(SQLType.Int), ["primary key", "not null", "AUTO_INCREMENT"]),
            Username = Column(ColumnType(SQLType.varchar, "30"), ["not null"]),
            Password = Column(ColumnType(SQLType.varchar, "64"), ["not null"])
        )
        db.close()

    def test_insert(self):
        db = Database(dbname, "127.0.0.1", "testing", "testing", "ORMDatabase")
        db.add_table("Users",
            id = Column(ColumnType(SQLType.Int), ["primary key", "not null", "AUTO_INCREMENT"]),
            Username = Column(ColumnType(SQLType.varchar, "30"), ["not null"]),
            Password = Column(ColumnType(SQLType.varchar, "64"), ["not null"])
        )
        db.tables["Users"].insert(
            columns=["Username", "Password"],
            parameters=["William", "Lim123"]
        ).execute()
        db.close()

    def test_select(self):
        db = Database(dbname, "127.0.0.1", "testing", "testing", "ORMDatabase")
        db.add_table("Users",
            id = Column(ColumnType(SQLType.Int), ["primary key", "not null", "AUTO_INCREMENT"]),
            Username = Column(ColumnType(SQLType.varchar, "30"), ["not null"]),
            Password = Column(ColumnType(SQLType.varchar, "64"), ["not null"])
        )
        self.assertEqual(db.tables["Users"].select().where(
            Equal("Username", "William").Or(
                Equal("Password", "William")
            )
        ).execute(), [(1, 'William', 'Lim123')])
        db.close()

    def test_update(self):
        db = Database(dbname, "127.0.0.1", "testing", "testing", "ORMDatabase")
        db.add_table("Users",
            id = Column(ColumnType(SQLType.Int), ["primary key", "not null", "AUTO_INCREMENT"]),
            Username = Column(ColumnType(SQLType.varchar, "30"), ["not null"]),
            Password = Column(ColumnType(SQLType.varchar, "64"), ["not null"])
        )
        db.tables["Users"].update(updates={
            "Username":"Alex"
        }).where(Equal("id", 1)).execute()
        db.close()

    def test_delete(self):
        db = Database(dbname, "127.0.0.1", "testing", "testing", "ORMDatabase")
        db.add_table("Users",
            id = Column(ColumnType(SQLType.Int), ["primary key", "not null", "AUTO_INCREMENT"]),
            Username = Column(ColumnType(SQLType.varchar, "30"), ["not null"]),
            Password = Column(ColumnType(SQLType.varchar, "64"), ["not null"])
        )
        db.tables["Users"].delete().where(Equal("id", 2)).execute()
        db.close()
    
from unittest import TestCase
import unittest
from src.TwigORM.database import ColumnType, Database, Column, ForeignKey, SQLType
from src.TwigORM.database.statement.comparison import Equal

unittest.TestLoader.sortTestMethodsUsing = None

dbname = "mysql"

class Testing(TestCase):

    def test_1drop(self):
        db = Database(dbname, "127.0.0.1", "testing", "testing", "ORMDatabase")
        db.drop("Post")
        db.drop("Users")
        db.close()
        

    def test_2createtable(self):
        db = Database(dbname, "127.0.0.1", "testing", "testing", "ORMDatabase")
        db.add_table("Users",
            id = Column(ColumnType(SQLType.Int), ["primary key", "not null", "AUTO_INCREMENT"]),
            Username = Column(ColumnType(SQLType.varchar, "30"), ["not null"]),
            Password = Column(ColumnType(SQLType.varchar, "64"), ["not null"])
        )
        db.close()

    def test_3insert(self):
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

    def test_4select(self):
        db = Database(dbname, "127.0.0.1", "testing", "testing", "ORMDatabase")
        db.add_table("Users",
            id = Column(ColumnType(SQLType.Int), ["primary key", "not null", "AUTO_INCREMENT"]),
            Username = Column(ColumnType(SQLType.varchar, "30"), ["not null"]),
            Password = Column(ColumnType(SQLType.varchar, "64"), ["not null"])
        )
        self.assertEqual(db.tables["Users"].select().where(
            Equal("Username", ["Alex"]).Or(
                Equal("Username", ["William"])
            )
        ).execute(), [(1, 'William', 'Lim123')])
        db.close()

    def test_5update(self):
        db = Database(dbname, "127.0.0.1", "testing", "testing", "ORMDatabase")
        db.add_table("Users",
            id = Column(ColumnType(SQLType.Int), ["primary key", "not null", "AUTO_INCREMENT"]),
            Username = Column(ColumnType(SQLType.varchar, "30"), ["not null"]),
            Password = Column(ColumnType(SQLType.varchar, "64"), ["not null"])
        )
        db.tables["Users"].update(updates={
            "Username":"Alex"
        }).where(Equal("id", [1])).execute()
        db.close()

    def test_6delete(self):
        db = Database(dbname, "127.0.0.1", "testing", "testing", "ORMDatabase")
        db.add_table("Users",
            id = Column(ColumnType(SQLType.Int), ["primary key", "not null", "AUTO_INCREMENT"]),
            Username = Column(ColumnType(SQLType.varchar, "30"), ["not null"]),
            Password = Column(ColumnType(SQLType.varchar, "64"), ["not null"])
        )
        db.tables["Users"].delete().where(Equal("id", [2])).execute()
        db.close()
    
    def test_7inner_join(self):
        db = Database(dbname, "127.0.0.1", "testing", "testing", "ORMDatabase")
        db.add_table("Users",
            id = Column(ColumnType(SQLType.integer), ["primary key", "not null", "AUTO_INCREMENT"]),
            Username = Column(ColumnType(SQLType.varchar, "30"), ["not null"]),
            Password = Column(ColumnType(SQLType.varchar, "64"), ["not null"])
        )
        db.add_table("Post",
            id = Column(ColumnType(SQLType.integer), ["primary key", "not null", "AUTO_INCREMENT"]),
            UserID = Column(ColumnType(SQLType.integer), ["not null"]),
            title = Column(ColumnType(SQLType.varchar, "100"), ["not null"]),
            body = Column(ColumnType(SQLType.text), ["not null"])
        )
        db.tables["Post"].drop()
        db.add_table("Post",
            [
                ForeignKey(["UserID"], "Users", ["id"])
            ],
            id = Column(ColumnType(SQLType.integer), ["primary key", "not null", "AUTO_INCREMENT"]),
            UserID = Column(ColumnType(SQLType.integer), ["not null"]),
            title = Column(ColumnType(SQLType.varchar, "100"), ["not null"]),
            body = Column(ColumnType(SQLType.text), ["not null"])
        )
        db.tables["Post"].insert(columns=["UserID", "title", "body"], parameters=[1, "This is a test Title.", "This is a test body."]).execute()
        self.assertEqual(
            db.tables["Users"].select(parameters=["Users.Username", "Post.title", "Post.body"]).inner_join("Post").on(Equal("Users.id", "Post.UserID")).execute(),
            [('Alex', 'This is a test Title.', 'This is a test body.')]
        )
        db.close()
from __future__ import annotations

from typing import Dict, List, Type, Union, TYPE_CHECKING


if TYPE_CHECKING:
    from .. import Table
    from .comparison import Comparison

class Statement:
    def __init__(self, table:Table) -> None:
        self.table = table
        self.declarations = []
        self.preparations = []
    
    def where(self, comparisons:Comparison) -> Type[Statement]:
        self.preparations.extend(comparisons.preparations)
        comparisons.db_type = self.table.database.db_type
        self.declarations += ["WHERE", comparisons.render()]
        return self

    def inner_join(self, table:str, alias:str = ""):
        self.declarations.append(f"""INNER JOIN {table}{f" AS {alias}" if alias != "" else ""}""")
        return self

    def left_join(self, table:str, alias:str = ""):
        self.declarations.append(f"""LEFT JOIN {table}{f" AS {alias}" if alias != "" else ""}""")
        return self

    def right_join(self, table:str, alias:str = ""):
        self.declarations.append(f"""RIGHT JOIN {table}{f" AS {alias}" if alias != "" else ""}""")
        return self

    def full_join(self, table:str, alias:str = ""):
        self.declarations.append(f"""FULL JOIN {table}{f" AS {alias}" if alias != "" else ""}""")
        return self

    def on(self, comparisons:Comparison) -> Type[Statement]:
        self.preparations.extend(comparisons.preparations)
        comparisons.db_type = self.table.database.db_type
        self.declarations += ["ON", comparisons.render()]
        return self

    def render(self):
        return " ".join(self.declarations)

    def execute(self):
        cur = self.table.database.connection.cursor()
        ret_val = []
        if self.table.database.db_type == "sqlite":
            cur.execute(self.render(), tuple(self.preparations))
        elif self.table.database.db_type == "mysql":
            cur.execute(self.render(), tuple(self.preparations))
        
        ret_val = cur.fetchall()
        cur.close()
        self.table.database.connection.commit()
        return ret_val

class Select(Statement):
    def __init__(self, table:Table, modifier:str = "", parameters:List[Union[str, Statement, tuple]] = ["*"], alias:str = "", additional_tables:List[str] = "") -> None:
        self.table = table
        params_list = []
        for param in parameters:
            if type(param) == str:
                params_list.append(param)
            if type(param) == Statement:
                params_list.append("(" + param.render() + ")")
            if type(param) == tuple:
                params_list.append(" ".join(param))
                
        self.declarations = ["SELECT", modifier, ", ".join(params_list), "FROM", table.table_name, ", " + ", ".join(additional_tables) if len(additional_tables) != 0 else "", f"AS {alias}" if alias != "" else ""]
        self.preparations = []

class Delete(Statement):
    def __init__(self, table:Table) -> None:
        self.table = table
        self.declarations = ["DELETE FROM", table.table_name]
        self.preparations = []

class Insert(Statement):
    def __init__(self, table:Table, modifier:str = "", columns:List[str] = [], parameters:List[Union[str, Statement]] = [], alias = "") -> None:
        self.table = table
        self.preparations = []
        self.render_preps = []
        self.alias = alias
        for param in parameters:
            if type(param) == Statement:
                self.preparations.extend(param.preparations)
                self.render_preps.append("(" + param.render() + ")")
            else:
                self.preparations.append(param)
                if table.database.db_type == "sqlite":
                    self.render_preps.append("?")
                elif table.database.db_type == "mysql":
                    self.render_preps.append("%s")
        self.declarations = [
            "INSERT", "" if modifier == "" else f"OR {modifier}", 
            "INTO", table.table_name, 
            "" if alias == "" else f"AS {alias}", 
            f"""({", ".join(columns)})""" if columns != [] else "", 
            "VALUES", "(" + ", ".join(self.render_preps) + ")"
            ]

class Update(Statement):
    def __init__(self, table:Table, modifier:str = "", updates:Dict[str, str | int | bool | Statement] = {}, alias = "") -> None:
        self.table = table
        self.preparations = []
        self.render_preps = []
        self.alias = alias
        for key, val in updates.items():
            if type(val) in [str, int, bool]:
                self.preparations.append(val)
                if table.database.db_type == "sqlite":
                    self.render_preps.append(f"{key} = ?")
                elif table.database.db_type == "mysql":
                    self.render_preps.append(f"{key} = %s")
            if type(val) == Statement:
                self.preparations.extend(val.preparations)
                self.render_preps.append(f"{key} = (" + val.render() + ")")
        self.declarations = ["UPDATE", "" if modifier == "" else f"OR {modifier}", table.table_name, "" if alias == "" else f"AS {alias}", "SET", ", ".join(self.render_preps)]
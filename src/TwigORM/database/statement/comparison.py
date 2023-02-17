from __future__ import annotations

from typing import Union, Tuple, Type, List, TYPE_CHECKING

from . import Statement

class Comparison:
    #CLASS IS DESIGNED TO BE INHERITED
    def __init__(self, lhs:Union[str, int, float, Comparison, Statement], rhs:Union[str, int, float, Comparison, Statement]) -> None:
        self.operator = ""
        self.preparations = []
        if type(lhs) == Statement:
            self.lhs = f"({lhs.render()})"
        else:
            self.lhs = lhs

        if type(rhs) == Statement:
            self.rhs = f"({rhs.render()})"
        elif type(rhs) == list:
            self.rhs = "?"
            self.db_type = "sqlite"
            self.preparations.append(rhs[0])
        else:
            self.rhs = rhs

        self.additions:List[Union[str, int, float, Comparison]] = []
    
    def Or(self, comparison:Type[Comparison] | Tuple[Comparison] | List[Comparison]):
        self.additions.append("OR")
        if issubclass(type(comparison), Comparison):
            self.preparations.extend(comparison.preparations)
            self.additions.append(comparison)
        elif type(comparison) == tuple or type(comparison) == list:
            self.preparations.extend(comparison[0].preparations)
            self.additions.extend(["(", comparison[0], ")"])
        return self

    def And(self, comparison:Type[Comparison] | Tuple[Comparison] | List[Comparison]):
        self.additions.append("AND")
        if issubclass(type(comparison), Comparison):
            self.preparations.extend(comparison.preparations)
            self.additions.append(comparison)
        elif type(comparison) == tuple or type(comparison) == list:
            self.preparations.extend(comparison[0].preparations)
            self.additions.extend(["(", comparison[0], ")"])
        return self

    def render(self) -> str:
        compiled_additions = ""
        
        for an, addition in enumerate(self.additions):
            if issubclass(type(addition), Comparison):
                if self.db_type == "mysql":
                    addition.db_type = self.db_type
                compiled_additions += f"{addition.render()}"
            else:
                compiled_additions += f"{addition}"
            if an != len(self.additions) - 1:
                compiled_additions += " "
                
        if self.rhs == "?":

            if self.db_type == "mysql":
                self.rhs = "%s"
            elif self.db_type == "sqlite":
                self.rhs = "?"
        
        return f"{self.lhs} {self.operator} {self.rhs} " + compiled_additions

class Equal(Comparison):
    def __init__(self, lhs: Union[str, int, float, Comparison, Statement], rhs: Union[str, int, float, Comparison, Statement]) -> None:
        super().__init__(lhs, rhs)
        self.operator = "="

class NotEqual(Comparison):
    def __init__(self, lhs: Union[str, int, float, Comparison, Statement], rhs: Union[str, int, float, Comparison, Statement]) -> None:
        super().__init__(lhs, rhs)
        self.operator = "!="

class LessThan(Comparison):
    def __init__(self, lhs: Union[str, int, float, Comparison, Statement], rhs: Union[str, int, float, Comparison, Statement]) -> None:
        super().__init__(lhs, rhs)
        self.operator = "<"

class GreaterThan(Comparison):
    def __init__(self, lhs: Union[str, int, float, Comparison, Statement], rhs: Union[str, int, float, Comparison, Statement]) -> None:
        super().__init__(lhs, rhs)
        self.operator = ">"

class GreaterEqual(Comparison):
    def __init__(self, lhs: Union[str, int, float, Comparison, Statement], rhs: Union[str, int, float, Comparison, Statement]) -> None:
        super().__init__(lhs, rhs)
        self.operator = ">="

class LessEqual(Comparison):
    def __init__(self, lhs: Union[str, int, float, Comparison, Statement], rhs: Union[str, int, float, Comparison, Statement]) -> None:
        super().__init__(lhs, rhs)
        self.operator = "<="

class In(Comparison):
    def __init__(self, lhs: Union[str, int, float, Comparison, Statement], rhs: Union[str, int, float, Comparison, Statement]) -> None:
        super().__init__(lhs, rhs)
        self.operator = "in"

class Like(Comparison):
    def __init__(self, lhs: Union[str, int, float, Comparison, Statement], rhs: Union[str, int, float, Comparison, Statement]) -> None:
        super().__init__(lhs, rhs)
        self.operator = "in"
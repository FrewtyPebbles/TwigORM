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
        else:
            self.rhs = "?"
            self.preparations.append(rhs)

        self.additions:List[Union[str, int, float, Comparison]] = []
    
    def Or(self, comparison:Type[Comparison] | Tuple[Comparison] | List[Comparison]):
        self.additions.append("OR")
        if issubclass(type(comparison), Comparison):
            self.preparations.extend(comparison.preparations)
            self.additions.append(comparison.render())
        elif type(comparison) == tuple or type(comparison) == list:
            self.preparations.extend(comparison[0].preparations)
            self.additions.append("(" + comparison[0].render() + ")")
        return self

    def And(self, comparison:Type[Comparison] | Tuple[Comparison] | List[Comparison]):
        self.additions.append("AND")
        if issubclass(type(comparison), Comparison):
            self.preparations.extend(comparison.preparations)
            self.additions.append(comparison.render())
        elif type(comparison) == tuple or type(comparison) == list:
            self.preparations.extend(comparison[0].preparations)
            self.additions.append("(" + comparison[0].render() + ")")
        return self

    def render(self) -> str:
        return f"{self.lhs} {self.operator} {self.rhs} " + " ".join(self.additions)

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
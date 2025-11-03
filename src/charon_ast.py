from dataclasses import dataclass
from typing import Any

# ---- Program / statements ----

@dataclass
class Program:
    items: list  # VarDecl or Stmt

@dataclass
class VarDecl:
    name: str
    type_name: str  # "Boolean" or "Char"

@dataclass
class Assign:
    name: str
    expr: Any

@dataclass
class Print:
    expr: Any

@dataclass
class If:
    cond: Any
    then_branch: list
    else_branch: list

@dataclass
class While:
    cond: Any
    body: list

# ---- Expressions ----

@dataclass
class Ident:
    name: str

@dataclass
class BoolLit:
    value: bool

@dataclass
class CharLit:
    value: str  

@dataclass
class Call:
    name: str
    arg: Any

@dataclass
class Binary:
    op: str     
    left: Any
    right: Any

@dataclass
class ArrayType:
    def __init__(self, size, elem_type):
        self.size = size
        self.elem_type = elem_type

@dataclass
class ArrayAccess:
    def __init__(self, name, index_expr):
        self.name = name
        self.index_expr = index_expr

@dataclass
class IntLit:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"IntLit({self.value})"


@dataclass
class MethodDecl:
    def __init__(self, name, body):
        self.name = name
        self.body = body  

@dataclass
class MethodCall:
    def __init__(self, name):
        self.name = name

# charon_ast.py
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
    then_branch: list  # list of statements/expr-stmts
    else_branch: list  # list of statements/expr-stmts

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
    value: str  # you can store the raw "'A'" literal or unescape to "A"

@dataclass
class Call:
    name: str
    arg: Any

@dataclass
class Binary:
    op: str      # "or","and","=","<","<=",">",">=","+"
    left: Any
    right: Any

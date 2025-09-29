from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class Node:
    pass

@dataclass
class Program(Node):
    items: List[Any]  # VarDecl or Stmt

@dataclass
class VarDecl(Node):
    name: str
    type_name: str

@dataclass
class Assign(Node):
    name: str
    expr: Any

@dataclass
class Print(Node):
    expr: Any

@dataclass
class If(Node):
    cond: Any
    then_branch: List[Any]
    else_branch: List[Any]

@dataclass
class While(Node):
    cond: Any
    body: List[Any]

# Expr nodes
@dataclass
class Ident(Node):
    name: str

@dataclass
class BoolLit(Node):
    value: bool

@dataclass
class CharLit(Node):
    value: str

@dataclass
class Binary(Node):
    op: str
    left: Any
    right: Any

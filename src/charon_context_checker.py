from charon_ast import *

class ContextChecker:
    def __init__(self):
        self.symbol_table = {}
        self.errors = []

    def error(self, message):
        self.errors.append(message)
        print(f"[Semantic Error] {message}")

    # program check 
    def check_program(self, program):
        for item in program.items:
            if isinstance(item, VarDecl):
                self.check_var_decl(item)
            else:
                self.check_stmt(item)

        if not self.errors:
            print("Context check passed — no semantic errors.")
        else:
            print(f"{len(self.errors)} semantic error(s) found.")

    # Variable declaration
    def check_var_decl(self, decl):
        if decl.name in self.symbol_table:
            self.error(f"Variable '{decl.name}' already declared.")
        else:
            self.symbol_table[decl.name] = decl.type_name

    # Statements
    def check_stmt(self, stmt):
        if isinstance(stmt, Assign):
            self.check_assign(stmt)
        elif isinstance(stmt, If):
            self.check_if(stmt)
        elif isinstance(stmt, Print):
            self.check_print(stmt)
        elif isinstance(stmt, While):
            self.check_while(stmt)
        else:
            self.error(f"Unknown statement type: {type(stmt).__name__}")

    def check_assign(self, stmt):
        if stmt.name not in self.symbol_table:
            self.error(f"Variable '{stmt.name}' not declared before assignment.")
            return

        lhs_type = self.symbol_table[stmt.name]
        rhs_type = self.infer_expr_type(stmt.expr)

        if lhs_type != rhs_type:
            self.error(f"Type mismatch in assignment: {stmt.name} ({lhs_type}) := ({rhs_type}).")

    def check_if(self, stmt):
        cond_type = self.infer_expr_type(stmt.cond)
        if cond_type != "Boolean":
            self.error("Condition in 'if' must be Boolean.")
        for s in stmt.then_branch:
            self.check_stmt(s)
        for s in stmt.else_branch:
            self.check_stmt(s)

    def check_while(self, stmt):
        cond_type = self.infer_expr_type(stmt.cond)
        if cond_type != "Boolean":
            self.error("Condition in 'while' must be Boolean.")
        for s in stmt.body:
            self.check_stmt(s)

    def check_print(self, stmt):
        self.infer_expr_type(stmt.expr)

    # Expression type inference
    def infer_expr_type(self, expr):
        if isinstance(expr, BoolLit):
            return "Boolean"
        elif isinstance(expr, CharLit):
            return "Char"
        elif isinstance(expr, Ident):
            if expr.name not in self.symbol_table:
                self.error(f"Variable '{expr.name}' used before declaration.")
                return "Unknown"
            return self.symbol_table[expr.name]
        elif isinstance(expr, Binary):
            left = self.infer_expr_type(expr.left)
            right = self.infer_expr_type(expr.right)
            op = expr.op

            if op in ["and", "or"]:
                if left == right == "Boolean":
                    return "Boolean"
                self.error(f"Invalid operands for '{op}': {left}, {right}")
                return "Unknown"
            elif op in ["=", "<", "<=", ">", ">="]:
                if left == right:
                    return "Boolean"
                self.error(f"Incompatible types for '{op}': {left}, {right}")
                return "Unknown"
            elif op == "+":
                if left == right == "Char":
                    return "Char"
                self.error(f"Invalid operands for '+': {left}, {right}")
                return "Unknown"
        else:
            self.error(f"Unknown expression type: {type(expr).__name__}")
            return "Unknown"

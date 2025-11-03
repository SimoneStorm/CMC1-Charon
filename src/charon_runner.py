from charon_ast import *

class Runner:
    def __init__(self):
        self.vars = {}
        self.methods = {}

    def run_program(self, program):
        for item in program.items:
            if isinstance(item, MethodDecl):
                self.methods[item.name] = item

        for item in program.items:
            if isinstance(item, VarDecl):
                if isinstance(item.type_name, ArrayType):
                    size = item.type_name.size
                    # Pre-fill array with None values
                    self.vars[item.name] = [None for _ in range(size)]
                else:
                    self.vars[item.name] = None

        for item in program.items:
            if not isinstance(item, (VarDecl, MethodDecl)):
                self.exec_stmt(item)


    # ---- statement execution ----
    def exec_stmt(self, stmt):
        if isinstance(stmt, VarDecl):
            self.vars[stmt.name] = None
        elif isinstance(stmt, Assign):
            self.exec_assign(stmt)
        elif isinstance(stmt, Print):
            val = self.eval_expr(stmt.expr)
            print(val)
        elif isinstance(stmt, If):
            cond = self.eval_expr(stmt.cond)
            branch = stmt.then_branch if cond else stmt.else_branch
            for s in branch:
                self.exec_stmt(s)
        elif isinstance(stmt, While):
            while self.eval_expr(stmt.cond):
                for s in stmt.body:
                    self.exec_stmt(s)
        elif isinstance(stmt, MethodCall):
            self.exec_method_call(stmt)
        else:
            raise RuntimeError(f"Unknown statement type {type(stmt).__name__}")

    # ---- assignment ----
    def exec_assign(self, stmt):
        if isinstance(stmt.name, ArrayAccess):
            arr_name = stmt.name.name
            index = self.eval_expr(stmt.name.index_expr)
            value = self.eval_expr(stmt.expr)
            self.vars[arr_name][index] = value
        else:
            name = stmt.name
            value = self.eval_expr(stmt.expr)
            self.vars[name] = value

    # ---- method call ----
    def exec_method_call(self, call):
        if call.name not in self.methods:
            raise RuntimeError(f"Unknown method {call.name}")
        method = self.methods[call.name]
        for stmt in method.body:
            self.exec_stmt(stmt)

    # ---- expression evaluation ----
    def eval_expr(self, expr):
        if isinstance(expr, BoolLit):
            return expr.value
        if isinstance(expr, CharLit):
            return expr.value.strip('"').strip("'")
        if isinstance(expr, IntLit):
            return expr.value
        if isinstance(expr, Ident):
            return self.vars.get(expr.name, None)
        if isinstance(expr, ArrayAccess):
            arr = self.vars.get(expr.name, [])
            index = self.eval_expr(expr.index_expr)
            return arr[index]
        if isinstance(expr, Binary):
            left = self.eval_expr(expr.left)
            right = self.eval_expr(expr.right)
            if expr.op == "and":  return left and right
            if expr.op == "or":   return left or right
            if expr.op == "+":    return str(left) + str(right)
            if expr.op == "=":    return left == right
            if expr.op == "<":    return left < right
            if expr.op == ">":    return left > right
        raise RuntimeError(f"Unknown expr {type(expr).__name__}")

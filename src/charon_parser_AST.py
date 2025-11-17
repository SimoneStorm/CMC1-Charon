# Parser from a list of tokens → an AST (abstract syntax tree).
from Scanner import scan
from charon_ast import *

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # ---------- utils ----------
    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        t = self.tokens[self.pos]
        self.pos += 1
        return t

    def accept(self, *types):
        if self.peek().type in types:
            return self.advance()
        return None

    def expect(self, *types):
        t = self.peek()
        if t.type in types:
            return self.advance()
        raise ParseError(f"Expected {'/'.join(types)} but got {t.type} at {t.line}:{t.col}")

    # ---------- top ----------
    def parse_program(self):
        items = []
        while self.peek().type != "EOF":
            # ---- METHOD SUPPORT ----
            if self.peek().type == "METHOD":
                items.append(self.parse_method_decl())
            elif self.peek().type == "VAR":
                items.append(self.parse_vardecl())
            else:
                items.append(self.parse_statement())
        return Program(items)

    def parse_vardecl(self):
        self.expect("VAR")
        name = self.expect("IDENT").value
        self.expect("COLON")

        # ---- ARRAY SUPPORT ----
        if self.accept("ARRAY"):
            self.expect("LBRACKET")
            size_token = self.expect("INT_LIT")
            self.expect("RBRACKET")
            self.expect("OF")
            elem_type = self.expect("BOOLEAN", "CHAR").value
            var_type = ArrayType(int(size_token.value), elem_type)
        else:
            tkn = self.expect("BOOLEAN", "CHAR")
            var_type = tkn.value

        self.expect("SEMICOLON")
        return VarDecl(name, var_type)

    # ---- METHOD DECLARATION ----
    def parse_method_decl(self):
        self.expect("METHOD")
        name = self.expect("IDENT").value
        self.expect("LPAREN")
        self.expect("RPAREN")
        body = []
        while self.peek().type not in ("END", "EOF"):
            body.append(self.parse_statement())
        self.expect("END")
        self.expect("SEMICOLON")
        return MethodDecl(name, body)

    # ---------- statements ----------
    def parse_statement(self):
        tok = self.peek()

        if tok.type == "IDENT":
            next_tok = self.tokens[self.pos + 1]
            if next_tok.type in ("ASSIGN", "LBRACKET"):
                return self.parse_assign()

        if tok.type == "PRINT":
            return self.parse_print()

        if tok.type == "IF":
            return self.parse_if()

        if tok.type == "WHILE":
            return self.parse_while()


        expr = self.parse_expr()
        self.expect("SEMICOLON")
        return expr

    def parse_assign(self):
        name = self.expect("IDENT").value
        if self.accept("LBRACKET"):
            index_expr = self.parse_expr()
            self.expect("RBRACKET")
            left = ArrayAccess(name, index_expr)
        else:
            left = name

        self.expect("ASSIGN")
        expr = self.parse_expr()
        self.expect("SEMICOLON")
        return Assign(left, expr)


    def parse_print(self):
        self.expect("PRINT")
        self.expect("LPAREN")
        e = self.parse_expr()
        self.expect("RPAREN")
        self.expect("SEMICOLON")
        return Print(e)

    def parse_if(self):
        self.expect("IF")
        cond = self.parse_expr()
        self.expect("THEN")
        then_branch = []
        while self.peek().type not in ("ELSE", "END", "EOF"):
            then_branch.append(self.parse_statement())
        else_branch = []
        if self.accept("ELSE"):
            while self.peek().type not in ("END", "EOF"):
                else_branch.append(self.parse_statement())
        self.expect("END")
        self.expect("SEMICOLON")
        return If(cond, then_branch, else_branch)

    def parse_while(self):
        self.expect("WHILE")
        cond = self.parse_expr()
        self.expect("DO")
        body = []
        while self.peek().type not in ("END", "EOF"):
            body.append(self.parse_statement())
        self.expect("END")
        self.expect("SEMICOLON")
        return While(cond, body)

    # ---------- expressions with precedence ----------
    def parse_expr(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()
        while self.accept("OR"):
            right = self.parse_and()
            left = Binary("or", left, right)
        return left

    def parse_and(self):
        left = self.parse_rel()
        while self.accept("AND"):
            right = self.parse_rel()
            left = Binary("and", left, right)
        return left

    def parse_rel(self):
        left = self.parse_add()
        t = self.peek()
        if t.type in ("EQ", "LT", "LE", "GT", "GE"):
            op = self.advance().value
            right = self.parse_add()
            return Binary(op, left, right)
        return left

    def parse_add(self):
        left = self.parse_primary()
        while self.accept("PLUS"):
            right = self.parse_primary()
            left = Binary("+", left, right)
        return left

    def parse_primary(self):
        t = self.peek()

        if t.type == "IDENT":
            name = self.advance().value
            
       
            if self.accept("LBRACKET"):
                index_expr = self.parse_expr()
                self.expect("RBRACKET")
                return ArrayAccess(name, index_expr)

            if self.accept("LPAREN"):
                self.expect("RPAREN")
                return MethodCall(name)
            return Ident(name)

        if t.type == "CHAR_LIT":
            self.advance()
            return CharLit(t.value)

        if t.type == "INT_LIT":
            self.advance()
            return IntLit(int(t.value))

        if t.type == "TRUE":
            self.advance()
            return BoolLit(True)

        if t.type == "FALSE":
            self.advance()
            return BoolLit(False)

        if t.type == "LPAREN":
            self.advance()
            e = self.parse_expr()
            self.expect("RPAREN")
            return e

        raise ParseError(f"Unexpected token {t.type} at {t.line}:{t.col}")


def parse_code(code: str):
    tokens = scan(code)
    p = Parser(tokens)
    return p.parse_program()

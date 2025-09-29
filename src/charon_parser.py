from lexer import Token, lex
from charon_ast import *  

# Custom parse error when tokens dont match the grammar
class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):  # Initialize the parser with a list of tokens
        self.tokens = tokens
        self.pos = 0 # Current position in the token list

    def peek(self): # Look at the current token without consuming it
        return self.tokens[self.pos]

    def advance(self): # Consume the current token
        t = self.tokens[self.pos] # Get current token
        self.pos += 1 # Move to the next token
        return t # Return the consumed token

    def accept(self, *types):
        if self.peek().type in types:
            return self.advance()
        return None

    def expect(self, *types):
        t = self.peek()
        if t.type in types:
            return self.advance()
        raise ParseError(
            f"Expected {'/'.join(types)} but got {t.type} at {t.line}:{t.col}"
        )


# Parsing program
    def parse_program(self): 
        items = []
        while self.peek().type != "EOF": # Loop until end of file
            if self.peek().type == "VAR": 
                items.append(self.parse_vardecl())
            else:
                items.append(self.parse_statement())
        return Program(items)

    def parse_vardecl(self):
        self.expect("VAR")
        name = self.expect("IDENT").value
        self.expect("COLON")
        tkn = self.expect("BOOLEAN", "CHAR")
        self.expect("SEMICOLON")
        return VarDecl(name, tkn.value) # Return a VarDecl node


# Parsing statements
    def parse_statement(self): #Decide which statement to parse based on the current token
        tok = self.peek()
        if tok.type == "IDENT" and self.tokens[self.pos + 1].type == "ASSIGN":
            return self.parse_assign()
        if tok.type == "PRINT":
            return self.parse_print()
        if tok.type == "IF":
            return self.parse_if()
        if tok.type == "WHILE":
            return self.parse_while()
        
        expr = self.parse_expr()
        self.expect("SEMICOLON")
        return expr # Expression statement



    def parse_assign(self):
        name = self.expect("IDENT").value
        self.expect("ASSIGN")
        expr = self.parse_expr()
        self.expect("SEMICOLON")
        return Assign(name, expr)

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






# Parsing expressions
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
            if self.accept("LPAREN"):
                arg = self.parse_expr()
                self.expect("RPAREN")
                return Binary("call_" + name, arg, None)
            return Ident(name)
        if t.type == "CHAR_LIT":
            self.advance()
            return CharLit(t.value)
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
        raise ParseError(
            f"Unexpected token {t.type} at {t.line}:{t.col}"
        )


# Helper to parse a string of source code
def parse_code(code: str):
    tokens = lex(code)
    p = Parser(tokens)
    return p.parse_program()

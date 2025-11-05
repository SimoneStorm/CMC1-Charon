# The Scanner cleans up the raw input; The first step
import re
from dataclasses import dataclass
from typing import List

#Defines what a token is
@dataclass
class Token:
    type: str #What kind of token it is (Assign, if osv)
    value: str
    line: int
    col: int
    pos: int

    def __repr__(self):
        return f"{self.type}({self.value!r}, l={self.line}, c={self.col})"

#List of token types that explains what they look like
TOKEN_SPEC = [
    ("COMMENT",    r"//[^\n]*"), #Starts with // continue until new line
    ("WHITESPACE", r"[ \t\r\n]+"),
    ("ASSIGN",     r":="), #Assignment operator
    ("LE",         r"<="), #Less Than or equal
    ("GE",         r">="),
    ("CHAR_LIT",   r'"[^"\n]*"|\'[^\'\n]*\''),
    ("INT_LIT",    r"[0-9]+"),
    ("IDENT",      r"[A-Za-z_][A-Za-z0-9_]*"),
    ("EQ",         r"="),
    ("LT",         r"<"),
    ("GT",         r">"),
    ("PLUS",       r"\+"),
    ("COLON",      r":"),
    ("SEMICOLON",  r";"),
    ("LPAREN",     r"\("),
    ("RPAREN",     r"\)"),
    ("COMMA",      r","),
    ("LBRACKET",   r"\["),
    ("RBRACKET",   r"\]"),
    ("UNKNOWN",    r"."),
]


# merges all token patterns into one big regex/dictionary
MASTER = re.compile("|".join(f"(?P<{n}>{p})" for n, p in TOKEN_SPEC))

# Special words that have meaning in my language
KEYWORDS = {
    "var":"VAR", "if":"IF", "then":"THEN", "else":"ELSE", "end":"END",
    "while":"WHILE","do":"DO","print":"PRINT",
    "Boolean":"BOOLEAN","Char":"CHAR","True":"TRUE","False":"FALSE",
    "or":"OR","and":"AND", "return":"RETURN", "func":"FUNC", "array":"ARRAY", "of":"OF", "method":"METHOD"

}

# takes the raw source code string (like "var x := 4711;") and turns it into a list of Token objects, one for each recognized symbol in the language
def scan(code: str) -> List[Token]:
    tokens = []
    line = 1
    col = 1
    pos = 0
    #This iterates over every regex match in the code string, in order.
    for m in MASTER.finditer(code): # The finditer() function walks through the entire input string and returns one match object per token.”
        kind = m.lastgroup
        txt = m.group()
        start = m.start()
        #Error check (If the starting post isnt the same as where we left of, it means there is an error)
        if start != pos:
            gap = code[pos:start]
            raise RuntimeError(f"Lexer gap at {pos}: {gap!r}")
        token_line, token_col = line, col
        # Update line and column counter
        if "\n" in txt:
            parts = txt.split("\n")
            line += len(parts)-1
            col = len(parts[-1]) + 1
        else:
            col += len(txt)
        pos = m.end()

        # Skip whitespace and comments
        if kind in ("WHITESPACE","COMMENT"): 
            continue
            
        # Handle identifiers and keywords

        #All words that look like identifiers are checked against a keyword table.
        #If the word matches a reserved keyword like if or while, the token type is changed.
        #If not, its treated as a normal identifier, such as a variable name

        if kind == "IDENT":
            mapped = KEYWORDS.get(txt)
            if mapped:
                tokens.append(Token(mapped, txt, token_line, token_col, start))
            else:
                tokens.append(Token("IDENT", txt, token_line, token_col, start))
            continue
        if kind == "CHAR_LIT":
            tokens.append(Token("CHAR_LIT", txt, token_line, token_col, start))
            continue
        if kind == "UNKNOWN":
            tokens.append(Token("UNKNOWN", txt, token_line, token_col, start))
            continue
        tokens.append(Token(kind, txt, token_line, token_col, start))


    tokens.append(Token("EOF","",line,col,pos)) # End-of-file token so parser knows when to stop
    return tokens


# Test code
if __name__ == "__main__":
    code = 'print("Cat is running");'
    for t in lex(code):
        print(t)

# Translator from a messy string of characters → a clean, typed list of tokens for the parser.
import re
from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    type: str
    value: str
    line: int
    col: int
    pos: int

    def __repr__(self):
        return f"{self.type}({self.value!r}, l={self.line}, c={self.col})"

TOKEN_SPEC = [
    ("COMMENT",    r"//[^\n]*"),
    ("WHITESPACE", r"[ \t\r\n]+"),
    ("ASSIGN",     r":="),
    ("LE",         r"<="),
    ("GE",         r">="),
    ("CHAR_LIT",   r"'([^'\\]|\\.)'"),
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
    ("UNKNOWN",    r"."),
]

MASTER = re.compile("|".join(f"(?P<{n}>{p})" for n, p in TOKEN_SPEC))

KEYWORDS = {
    "var":"VAR", "if":"IF", "then":"THEN", "else":"ELSE", "end":"END",
    "while":"WHILE","do":"DO","print":"PRINT",
    "Boolean":"BOOLEAN","Char":"CHAR","True":"TRUE","False":"FALSE",
    "or":"OR","and":"AND", "return":"RETURN", "func":"FUNC"
}

def lex(code: str) -> List[Token]:
    tokens = []
    line = 1
    col = 1
    pos = 0
    for m in MASTER.finditer(code):
        kind = m.lastgroup
        txt = m.group()
        start = m.start()
        if start != pos:
            # Should not happen if regex covers all characters
            gap = code[pos:start]
            raise RuntimeError(f"Lexer gap at {pos}: {gap!r}")
        token_line, token_col = line, col
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

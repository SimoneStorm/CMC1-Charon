from charon_parser import parse_code
from charon_ast import Program
import sys, json

EXAMPLE = """
var x : Boolean;
x := True;
print(x);
"""

if __name__ == "__main__":
    prog = parse_code(EXAMPLE)
    
    import ast as pyast
    from ast import *
    def pretty(node, indent=0):
        pad = "  "*indent
        if node is None: return pad + "None\n"
        if hasattr(node, "__dict__"):
            s = pad + node.__class__.__name__ + "\n"
            for k,v in node.__dict__.items():
                if isinstance(v, list):
                    s += pad + "  " + k + ":\n"
                    for it in v:
                        s += pretty(it, indent+2)
                else:
                    s += pad + "  " + f"{k}: {v}\n"
            return s
        return pad + repr(node) + "\n"
    print(pretty(prog))

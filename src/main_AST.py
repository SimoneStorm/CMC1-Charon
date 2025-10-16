# main.py
from charon_parser_AST import parse_code
from charon_context_checker import ContextChecker



#AST example

EXAMPLE = """
var x : Boolean;
var c : Char;
x := True;
c := 'A';

if x and (c = 'A' or True) then
    print(c);
else
    c := c + 'B';
end;

while x do
    print(c);
end;
"""



def Tree(node, indent=0): 
    pad = "  " * indent 
    if node is None: 
        return pad + "None\n"
    if hasattr(node, "__dict__"):
        s = pad + node.__class__.__name__ + "\n"
        for k, v in node.__dict__.items():
            if isinstance(v, list):
                s += pad + f"  {k}:\n"
                for it in v:
                    s += Tree(it, indent + 2)
            else:
                if hasattr(v, "__dict__"):
                    s += pad + f"  {k}:\n" + Tree(v, indent + 2)
                else:
                    s += pad + f"  {k}: {repr(v)}\n"
        return s
    return pad + repr(node) + "\n"

if __name__ == "__main__":
    ast = parse_code(EXAMPLE)
    print(Tree(ast))







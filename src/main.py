from charon_parser_AST import parse_code
from charon_context_checker import ContextChecker

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

if __name__ == "__main__":
    print("Parsing program...")
    program_ast = parse_code(EXAMPLE)

    print("\nRunning context checker...")
    checker = ContextChecker()
    checker.check_program(program_ast)

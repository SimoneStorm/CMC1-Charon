from charon_parser_AST import parse_code
from charon_context_checker import ContextChecker

EXAMPLE = """
method Cat()
    print("Cat is running");
    Dog();
end;

method Dog()
    print("Dog says woof");
end;

var MyArray : array[5] of Char;
MyArray[1] := "A";
print(MyArray[1]);

Cat();
"""


if __name__ == "__main__":
    print("Parsing program...")
    program_ast = parse_code(EXAMPLE)

    print("\nRunning context checker...")
    checker = ContextChecker()
    checker.check_program(program_ast)

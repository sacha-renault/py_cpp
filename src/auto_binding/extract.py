import clang.cindex
from clang.cindex import CursorKind
import sys
sys.path.insert(0, "/home/wsl/Projects_code/py_cpp/src/")
from auto_binding.types import CxxClass, CxxFunction, CxxTemplateFunction

clang.cindex.Config.set_library_file('/usr/lib/llvm-12/lib/libclang-12.so')  # Set this to your actual path


def parse_func(node):
        if node.kind == CursorKind.FUNCTION_DECL or node.kind == CursorKind.CXX_METHOD:
            func = CxxFunction(
                node,
                node.spelling, 
                [list(param.get_tokens()) for param in node.get_arguments()])
        
        elif node.kind == CursorKind.FUNCTION_TEMPLATE:
            func = CxxTemplateFunction(
                node,
                node.spelling, 
                [list(param.get_tokens()) for param in node.get_children()])
        else:
            raise ValueError("Unknown function kind")
        
        return func


def extract_all(header_file):
    index = clang.cindex.Index.create()

    translation_unit = index.parse(header_file, args=['-std=c++17'])

    functions = []
    classes = []
    
    def visit_node(node):
        if (node.kind == CursorKind.FUNCTION_DECL or
            node.kind == CursorKind.FUNCTION_TEMPLATE):
            func = parse_func(node)
            functions.append(func)
        
        elif node.kind == CursorKind.CLASS_DECL:
            class_ = CxxClass(node, node.spelling)
            for child in node.get_children():
                if node.spelling == "func1":
                    print(node.kind)
                if (child.kind == CursorKind.CXX_METHOD or
                    node.kind == CursorKind.FUNCTION_TEMPLATE):
                    method = parse_func(child)
                    class_.add_methods(method)
            classes.append(class_)
        
        # Continue visiting other nodes
        for child in node.get_children():
            visit_node(child)

    visit_node(translation_unit.cursor)
    return functions, classes

# Example usage
header_file = "/home/wsl/Projects_code/py_cpp/.examples/cumulative (overload)/binding.cpp"
header_file = "/home/wsl/Projects_code/py_cpp/.examples/game_of_life (openMP)/life_game/binding.cpp"

functions, classes = extract_all(header_file)
# results = extract_all("/home/wsl/Projects_code/py_cpp/.examples/game_of_life (openMP)/life_game/src/Grid.cpp")

print("Functions:")
for func in functions:
    print(f"  {func}")

print("\nClasses and Methods:")
for class_ in classes:
    print(f"Class: {class_.name}")
    print("  Methods:")
    for method in class_.methods:
        print(f"    {method}")
#     print("  Public Methods:")
#     for pub_method in details['public_methods']:
#         print(f"    {pub_method}")

    

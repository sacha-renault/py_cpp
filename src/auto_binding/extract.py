import clang.cindex
from clang.cindex import TokenKind, CursorKind
import sys
sys.path.insert(0, "/home/wsl/Projects_code/py_cpp/src/")
from auto_binding.types import CxxClass, CxxFunction

clang.cindex.Config.set_library_file('/usr/lib/llvm-12/lib/libclang-12.so')  # Set this to your actual path


def get_raw_type_string(lines, param):
    # Retrieve the source code range corresponding to the parameter
    start = param.extent.start
    end = param.extent.end

    # Extract the exact text corresponding to the extent
    raw_text = "".join(lines[start.line - 1:end.line])
    raw_text = raw_text[start.column - 1:end.column - 1]
    raw_text = raw_text.strip()
    return " ".join(raw_text.split(" ")[:-1])

def get_type(cursor):
    arg_type = ""
    tokens = list(cursor.get_tokens())[:-1]
    for i in range(len(tokens)):
        token = tokens[i]
        if i == 0 or not (token.kind == TokenKind.PUNCTUATION or tokens[i-1].kind == TokenKind.PUNCTUATION):
            arg_type += " "
        arg_type += token.spelling
    return arg_type.strip()


def parse_func(node):
        if node.kind == CursorKind.FUNCTION_DECL:
            func = CxxFunction(
                node.spelling, 
                False, # If the function has template !
                [get_type(param) for param in node.get_arguments()])
        
        elif node.kind == CursorKind.FUNCTION_TEMPLATE:
            func = CxxFunction(
                node.spelling, 
                True,
                [get_type(param) for param in list(node.get_children())[1:]])
        
        elif node.kind == CursorKind.TEMPLATE_REF:
            node
            func = None
        return func


def extract_functions_classes_and_methods(header_file):
    index = clang.cindex.Index.create()

    translation_unit = index.parse(header_file, args=['-std=c++17'])

    results = {
        'functions': [],
        'classes': []
    }
    
    def visit_node(node, results):
        if node.kind == CursorKind.TEMPLATE_REF:
            print("UAfyberzt")
        if (node.kind == CursorKind.FUNCTION_DECL or
            node.kind == CursorKind.FUNCTION_TEMPLATE or
            node.kind == CursorKind.TEMPLATE_REF):
            func = parse_func(node)
            results['functions'].append(func)
        
        elif node.kind == CursorKind.CLASS_DECL:
            pass
            # # Classes and their methods
            # class_name = node.spelling
            # if class_name:
            #     results['classes'][class_name] = []
            #     for child in node.get_children():
            #         if child.kind == clang.cindex.CursorKind.CXX_METHOD:
            #             method_signature = get_method_signature(child)
            #             results['classes'][class_name].append(method_signature)
        
        # Continue visiting other nodes
        for child in node.get_children():
            visit_node(child, results)

    def get_method_signature(node):
        return_type = node.result_type.spelling
        method_name = node.spelling
        params = [f'{param.type.spelling} {param.spelling}' for param in node.get_arguments()]
        param_list = ', '.join(params)
        signature = f'{return_type} {method_name}({param_list})'
        return signature

    visit_node(translation_unit.cursor, results)
    return results

# Example usage
header_file = "/home/wsl/Projects_code/py_cpp/.examples/game_of_life (openMP)/life_game/src/Grid.h"
results = extract_functions_classes_and_methods(header_file)

print("Functions:")
for func in results['functions']:
    print(f"  {func}")

# print("\nClasses and Methods:")
# for class_name, details in results['classes'].items():
#     print(f"Class: {class_name}")
#     print("  Methods:")
#     for method in details['methods']:
#         print(f"    {method}")
#     print("  Public Methods:")
#     for pub_method in details['public_methods']:
#         print(f"    {pub_method}")

    

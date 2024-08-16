from typing import List, Tuple
import clang.cindex
from clang.cindex import CursorKind
from .types import CxxClass, CxxFunction, CxxTemplateFunction

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


def extract_all(header_file, *args) -> Tuple[List[CxxFunction], List[CxxClass]]:
    index = clang.cindex.Index.create()

    translation_unit = index.parse(header_file, args=args)

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


import os
import tempfile
from glob import glob
from typing import List, Tuple

import clang.cindex
from clang.cindex import CursorKind

from ..data import __HEADERS_PATH__
from .types import CxxClass, CxxFunction, CxxTemplateFunction, CxxConstructor


def parse_func(node):
    if (node.kind == CursorKind.FUNCTION_DECL or 
        node.kind == CursorKind.CXX_METHOD):

        # Get function
        func = CxxFunction(
            node,
            node.spelling, 
            [list(param.get_tokens()) for param in node.get_arguments()], # Signature
            node.result_type)
        
    elif node.kind == node.kind == CursorKind.CONSTRUCTOR:
        func = CxxConstructor(
            node,
            node.spelling, 
            [list(param.get_tokens()) for param in node.get_arguments()], # Signature
            node.result_type)
    
    elif node.kind == CursorKind.FUNCTION_TEMPLATE:
        func = CxxTemplateFunction(
            node,
            node.spelling, 
            [list(param.get_tokens()) for param in node.get_children()], # Signature
            node.result_type)
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
                if (child.kind == CursorKind.CXX_METHOD or
                    node.kind == CursorKind.FUNCTION_TEMPLATE or
                    child.kind == CursorKind.CONSTRUCTOR):

                    # Get method and add to class
                    method = parse_func(child)
                    class_.add_methods(method)
                
            classes.append(class_)
        
        # Continue visiting other nodes
        for child in node.get_children():
            visit_node(child)

    visit_node(translation_unit.cursor)
    return functions, classes

def get_func_and_classes():
    with tempfile.NamedTemporaryFile('w+', suffix=".cpp", delete=True, dir='.') as tmp:
        # Get all files
        files = glob(__HEADERS_PATH__)

        # Set includes
        for file in files:
            path = os.path.normpath(file)
            tmp.write(f"#include \"{path}\"\n")

        # Seek back to start
        tmp.seek(0)

        # Into parser
        functions, classes = extract_all(tmp.name, '-std=c++17')

        # Get abs path
        abs_files = [os.path.abspath(file) for file in files]

        # filter functions that comes from the files
        functions = [func for func in functions if func.path in abs_files and not func.name.startswith("_")]

        # filter classes that comes from the files
        classes = [class_ for class_ in classes if class_.path in abs_files and not class_.name.startswith("_")]

    return functions, classes


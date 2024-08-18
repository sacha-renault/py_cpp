import os
from typing import List
from collections import defaultdict
import warnings

from .mapping import get_python_signature, get_python_return_type
from .extract import get_func_and_classes
from .templates import HintTemplate
from .utils import pascal_case_to_snake_case
from ..configuration import Config
from .types import (CxxBase, CxxClass, CxxConstructor, 
                    CxxFunction, CxxTemplateFunction)
from ..data import (__BINDING_TEMPLATE_PATH__, 
                    __HEADERS_PATH__,
                    __BINDING_INCLUDES__,
                    __BINDING_POSITION__,
                    __CONFIG_FILE_NAME__)

def get_function_hints(functions: List[CxxFunction], 
                         render_arg: bool, 
                         naming: str,
                         src_or_namespace: str = "",
                         indent: str = "\t") -> str:
    """Create the binding (as string) for the CxxFunction passed as argument.

    Args:
        functions (List[CxxFunction]): list of function that need bindings
        render_arg (bool): render argument (as method or as function)
        naming (str): naming for the comment
        src_or_namespace (str, optional): TODO will be removed over filed in CxxFunction. 
        Defaults to "".
        indent (str, optional): indent. Defaults to "\t".

    Raises:
        ValueError: Unknown CxxFunction subclass

    Returns:
        str: the string representation of the binding.
    """
    # init a dict to count number of occurence
    name_count = defaultdict(int)
    
    for func in functions:
        name_count[func.name] += 1

    # function definition
    func_binding = f"{indent}# {naming} DEFINITION \n"

    # NO OVERLOAD
    for func in functions:
        # Get name in snake case
        py_f_name = pascal_case_to_snake_case(func.name)

        # get python signature
        python_signature = get_python_signature(func.signature)

        # get python return type
        python_return_type = get_python_return_type(func.return_type)

        # init a binding template for the function
        template = HintTemplate(py_f_name, 
            python_signature, 
            python_return_type)

        # If template idk what to do still
        if isinstance(func, CxxTemplateFunction):
            warnings.warn("Template function aren't supported yet.")
            continue

        # If constructor we call py::init
        elif isinstance(func, CxxConstructor):
            template.set_constructor()

        # TODO
        # Detect when operator 
        # create a mapping and use template.set_function
        # with the correct python magic func 
        # __add__, __sub__ ...

        # else simple function
        elif isinstance(func, CxxFunction):
            if name_count[func.name] > 1:
                template.set_overload()

        else:
            raise ValueError(f"NOT A KNOWN TYPE : {type(func)}")
        
        func_binding += template.render_as(render_arg, indent)
        
        
    func_binding += "\n\n" # let some space after functino bindings are done
    return func_binding

def get_class_hints(classes: List[CxxClass]) -> str:
    """Create the binding (as string) for the CxxClass passed as argument.

    Args:
        classes (List[CxxClass]): list of class that needs bindings

    Returns:
        str: the string representation of the binding.
    """
    # function definition
    class_binding = "# CLASS DEFINITION \n"
    for class_ in classes:
        class_binding += f"class {class_.name}:\n"
        class_binding += get_function_hints(class_.methods, True, "METHODS", class_.name + "::","\t")
    return class_binding

def auto_hints(*_) -> str:
    """function that wraps all the autobinding process

    Returns:
        str: the string content for the binding.cpp file.
    """
    # Get template content
    content = "from typing import overload"

    # Get functions and classes
    functions, classes = get_func_and_classes()
    
    # make function binding
    f_hints = get_function_hints(functions, '', 'FUNCTION', indent="")
    if f_hints.replace("\n", "").strip() != "":
        content += "\n\n" + f_hints
    
    # make function binding
    c_hints = get_class_hints(classes)
    if c_hints.replace("\n", "").strip() != "":
        content += "\n\n" + c_hints

    # class definition
    return content
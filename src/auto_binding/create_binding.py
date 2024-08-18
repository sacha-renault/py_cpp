import os
from glob import glob
from typing import List
import warnings
from collections import defaultdict
from .templates import BindingTemplate
from .utils import pascal_case_to_snake_case
from .extract import get_func_and_classes
from .types import CxxFunction, CxxTemplateFunction, CxxClass, CxxConstructor
from ..configuration import Config
from ..data import (__BINDING_TEMPLATE_PATH__, 
                    __HEADERS_PATH__,
                    __BINDING_INCLUDES__,
                    __BINDING_POSITION__,
                    __CONFIG_FILE_NAME__)

def prepare_binding_template(package_dir: str) -> str:
    """get the template of the binding.cpp file as string

    Args:
        package_dir (str): the path where py_cpp is installed

    Returns:
        str: the content of the template file
    """
    path = os.path.join(package_dir, __BINDING_TEMPLATE_PATH__)
    with open(path, "r") as file:
        content = file.read()
    return content

def get_function_binding(functions: List[CxxFunction], 
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
    func_binding = f"{indent}// {naming} DEFINITION \n"

    # NO OVERLOAD
    for func in functions:
        # Get name in snake case
        py_f_name = pascal_case_to_snake_case(func.name)

        # Get the ref of the cpp function
        cpp_ref_name = f"&{src_or_namespace}{func.name}"

        # init a binding template for the function
        template = BindingTemplate(py_f_name, 
            cpp_ref_name, 
            func.get_signature_string(), 
            func.return_type)

        # If template idk what to do still
        if isinstance(func, CxxTemplateFunction):
            # TODO
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

def get_class_binding(classes: List[CxxClass]) -> str:
    """Create the binding (as string) for the CxxClass passed as argument.

    Args:
        classes (List[CxxClass]): list of class that needs bindings

    Returns:
        str: the string representation of the binding.
    """
    # function definition
    class_binding = "\t// CLASS DEFINITION \n"
    for class_ in classes:
        class_binding += f"\tpy::class_<{class_.name}>(m, \"{class_.name}\")\n"
        class_binding += get_function_binding(class_.methods, True, "METHODS", class_.name + "::","\t\t") + ";"
    return class_binding

def auto_bindings(call_dir: str, pycpp_dir: str) -> str:
    """function that wraps all the autobinding process

    Args:
        call_dir (str): where the cmd is called.
        package_dir (str): where pycpp is located.

    Returns:
        str: the string content for the binding.cpp file.
    """
    # Get template content
    content = prepare_binding_template(pycpp_dir)

    # include
    files = glob(__HEADERS_PATH__)

    # Get the config
    config = Config.load(os.path.join(call_dir, __CONFIG_FILE_NAME__))

    # Set includes
    for file in files:
        path = os.path.normpath(file)
        include_statement = f"#include \"{path}\""
        content = content.replace(__BINDING_INCLUDES__, f"{include_statement}\n{__BINDING_INCLUDES__}")
    
    # Replace the module name
    content = content.replace("%module_name%", config.name)

    # Get functions and classes
    functions, classes = get_func_and_classes()
    
    # make function binding
    content = content.replace(
        __BINDING_POSITION__, 
        f"{get_function_binding(functions, '', 'FUNCTION')}\n{__BINDING_POSITION__}")
    
    # make function binding
    content = content.replace(
        __BINDING_POSITION__, f"{get_class_binding(classes)}\n")

    # class definition
    return content
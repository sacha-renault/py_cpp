from clang.cindex import Type

__MAPPING__ = {
    "int": "int",
    "long": "int",
    "double": "float",
    "float": "float",
    "std::string" : "str",
    "char*": "str",
    "_T*": "List[_T]"
}

def get_python_signature(signature: list) -> str:
    python_signature_list = []
    for param in signature:
        *tokens, arg_name = param
        build_cpp_type = ""
        for token in tokens:
            spelling = token.spelling
            if spelling not in ("const", "&", "&&"):
                build_cpp_type += spelling

            
        python_signature = arg_name.spelling
        python_type = __MAPPING__.get(build_cpp_type.strip())
        if python_type != None:
               python_signature += ": " + python_type
        python_signature_list.append(python_signature)
    return ", ".join(python_signature_list)
        

def get_python_return_type(return_type) -> str:
    if return_type:
        return __MAPPING__.get(return_type.spelling.strip())
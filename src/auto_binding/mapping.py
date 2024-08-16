from clang.cindex import TypeKind

__MAPPING__ = {
    "int": "int",
    "long": "int",
    "double": "float",
    "float": "float",
    "std::string" : "str",
    "char*": "str",
    "_T*": "List[_T]"
}
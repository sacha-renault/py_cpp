from typing import Optional, Any
from .types import CxxBase, CxxFunction, CxxConstructor, CxxClass

class TemplateBase:
    def __init__(self, 
                 py_func_name: str, 
                 cpp_ref: str, 
                 signature: Optional[str] = None, 
                 return_type: Optional[str] = None) -> None:
        self.py_func_name = py_func_name
        self.cpp_ref = cpp_ref
        self.signature = signature if signature is not None else ""
        self.return_type = return_type
        self.is_constructor = False
        self.is_overload = False

    def set_overload(self) -> None:
        self.is_overload = True

    def set_constructor(self) -> None:
        self.is_constructor = True

    def set_py_func_name(self, new_name: str) -> None:
        self.py_func_name = new_name

    def render_as(self, is_method: bool, indent: str = "") -> str:
        raise NotImplementedError("Subclasses must implement this method")


class BindingTemplate(TemplateBase):
    def __init__(self, 
                 function_name: str, 
                 cpp_ref: str, 
                 signature: Optional[str] = None, 
                 return_type: Optional[str] = None) -> None:
        super().__init__(function_name, cpp_ref, signature, return_type)

    def render_as(self, is_method: bool, indent: str = "") -> str:
        result = f".def("

        args = [f"\"{self.py_func_name}\""]
        
        if self.is_overload:
            args.append(f"py::overload_cast<{self.signature}>({self.cpp_ref})")
        elif self.is_constructor:
            args = [f"py::init<{self.signature}>()"]
        else:
            args.append(self.cpp_ref)

        result += ", ".join(args) + ")"

        if not is_method:
            result = "m" + result + ";"
        return indent + result + "\n"


class HintTemplate(TemplateBase):
    def __init__(self, 
                 function_name: str, 
                 signature: Optional[str] = None, 
                 return_type: Optional[str] = None) -> None:
        super().__init__(function_name, "", signature, return_type)

    def render_as(self, is_method: bool, indent: str = "") -> str:
        result = f"def {self.py_func_name}("
        if self.signature:
            result += self.signature
        result += ")"
        if self.return_type:
            result += f" -> {self.return_type}"
        result += ": ..."
        if not is_method:
            result = "m" + result + ";"
        return indent + result + "\n"

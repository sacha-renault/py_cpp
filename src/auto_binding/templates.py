from .types import CxxBase, CxxFunction, CxxConstructor, CxxClass

class BindingTemplate:
    def __init__(self) -> None:
        self.value = ".def("

    def set_function(self, function_name: str, cpp_ref: str, *args) -> None:
        self.value += f"\"{function_name}\", {cpp_ref}" 
        if len(args) > 0:
            self.value += ", " + ", ".join(args)
        self.value += ")"

    def set_overload_function(self, function_name: str, cpp_ref: str, signature_str: str, *args) -> None:
        self.set_function(function_name, f"py::overload_cast<{signature_str}>({cpp_ref})", *args)

    def set_constructor(self, signature_str: str, *_):
        self.value += f"py::init<{signature_str}>())"

    def render_as(self, is_method, indent: str = "") -> str:
        if not is_method:
            self.value = "m" + self.value + ";"
        return indent + self.value + "\n"
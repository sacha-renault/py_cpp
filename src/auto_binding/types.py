
import typing

class CxxFunction:
    def __init__(self, name: str, is_template: bool = False, signature = None) -> None:
        self.name = name
        self.is_template: bool = is_template
        self.signature = signature if signature is not None else []
    
    def __str__(self) -> str:
        return f"<Function: {self.name}({', '.join(self.signature)}) - Template : {self.is_template}>"

class CxxClass:
    def __init__(self, name: str, is_template: bool = False) -> None:
        self.name = name
        self.is_template: bool = is_template
        self.methods: typing.List[CxxFunction] = []

    def add_methods(self, method: CxxFunction) -> None:
        self.methods.append(method)


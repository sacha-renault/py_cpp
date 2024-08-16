import typing
from .utils import tokens_to_string, split_template_normal, typename_template_to_string

class CxxFunction:
    def __init__(self, node, name: str, signature = None) -> None:
        self.node = node
        self.name = name
        self.signature = signature if signature is not None else []
    
    def __str__(self) -> str:
        return f"<Function: {self.name}({', '.join([tokens_to_string(s) for s in self.signature])})>"
    
class CxxTemplateFunction(CxxFunction):
    def __init__(self, 
                 node,
                 name: str, 
                 signature=None) -> None:
        template, non_template = split_template_normal(signature)
        super().__init__(node, name, non_template)
        self.template_param = template
    
    def __str__(self) -> str:
        return (f"<Function: {self.name}<{', '.join([typename_template_to_string(s) for s in self.template_param])}>"
                f"({', '.join([tokens_to_string(s) for s in self.signature])})>")

class CxxClass:
    def __init__(self, node, name: str) -> None:
        self.node = node
        self.name = name
        self.methods: typing.List[CxxFunction] = []

    def add_methods(self, method: CxxFunction) -> None:
        self.methods.append(method)


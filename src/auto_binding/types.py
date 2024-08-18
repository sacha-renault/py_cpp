import typing
from .utils import tokens_to_string, split_template_normal, typename_template_to_string

class CxxBase:
    @property
    def path(self) -> str:
        return self.node.location.file.name

class CxxFunction(CxxBase):
    def __init__(self, node, name: str, signature = None, return_type = None) -> None:
        self.node = node
        self.name = name
        self.signature = signature if signature is not None else []
        self.return_type = return_type
    
    def __str__(self) -> str:
        return f"<Function: {self.name}({self.get_signature_string()})>"
    
    def get_signature_string(self) -> str:
        return ', '.join([tokens_to_string(s) for s in self.signature])
    
class CxxConstructor(CxxFunction):
    pass
    
class CxxTemplateFunction(CxxFunction):
    def __init__(self, 
                 node,
                 name: str, 
                 signature=None,
                 return_type=None) -> None:
        template, non_template = split_template_normal(signature)
        super().__init__(node, name, non_template, signature, return_type)
        self.template_param = template
    
    def __str__(self) -> str:
        return (f"<Function: {self.name}<{', '.join([typename_template_to_string(s) for s in self.template_param])}>"
                f"({', '.join([tokens_to_string(s) for s in self.signature])})>")

class CxxClass(CxxBase):
    def __init__(self, node, name: str) -> None:
        self.node = node
        self.name = name
        self.methods: typing.List[CxxFunction] = []

    def add_methods(self, method: CxxFunction) -> None:
        self.methods.append(method)


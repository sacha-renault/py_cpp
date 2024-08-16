class Template:
    def __init__(self) -> None:
        self.datas = []

    def fill(self, *datas) -> None:
        for data in datas:
            self.datas.append(data)

    def render(self, is_method, indent) -> str:
        rendered = ".def(" + ", ".join(self.datas) + ")"
        if not is_method:
            rendered = "m" + rendered + ";"
        return indent + rendered + "\n"
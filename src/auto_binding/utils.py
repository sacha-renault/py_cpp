from typing import List, Tuple
from clang.cindex import TokenKind, CursorKind, Cursor
import re

def typename_template_to_string(tokens: List[Cursor]):
    return tokens[1].spelling

def tokens_to_string(tokens: List[Cursor]):
    arg_str = ""

    for i in range(len(tokens) - 1):
        token = tokens[i]
        if i == 0 or not (token.kind == TokenKind.PUNCTUATION or tokens[i-1].kind == TokenKind.PUNCTUATION):
            arg_str += " "
        arg_str += token.spelling
    return arg_str.strip()

def split_template_normal(types: List[List[Cursor]]) -> Tuple[List[List[Cursor]], List[List[Cursor]]]:
    template = []
    non_template = []

    for tokens in types:
        is_template = False
        for token in tokens:
            if token.kind == TokenKind.KEYWORD and token.spelling == "typename":
                template.append(tokens)
                is_template = True
        if not is_template:
            non_template.append(tokens)
    
    return template, non_template

def pascal_case_to_snake_case(func_name: str) -> str:
    snake_case_name = re.sub(r'(?<!^)(?=[A-Z])', '_', func_name).lower()
    return snake_case_name
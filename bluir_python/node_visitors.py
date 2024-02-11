import ast
import re
import string

import nltk


# 访问AST中的函数定义节点
class FuncVisitor(ast.NodeVisitor):
    # 定义一个空的函数列表，用于存储找到的所有函数
    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        ast.NodeVisitor.generic_visit(self, node)
    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)

# 访问AST中的类定义节点
class ClassVisitor(ast.NodeVisitor):
    def __init__(self):
        self.classes = []

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        ast.NodeVisitor.generic_visit(self, node)
    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)

# 访问AST中的标识符定义节点
class IdentifierVisitor(ast.NodeVisitor):
    def __init__(self):
        self.items = []

    def visit_Attribute(self, node):
        self.items.append(node.attr)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Name(self, node):
        self.items.append(node.id)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_keyword(self, node):
        self.items.append(node.arg)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_ClassDef(self, node):
        self.items.append(node.name)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        self.items.append(node.name)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_alias(self, node):
        self.items.append(node.name)
        ast.NodeVisitor.generic_visit(self, node)

    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)

def transform(text):
    text = re.sub(r'[^\w\s]', ' ', text)
    text = text.replace('_', ' ')
    splitted = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', text)).split()
    text = [w.lower() for w in splitted]
    res = ''
    for t in text:
        if len(t) > 2:
            res += t
            res += ' '
    return res


# # 读取Python代码文件，并解析为AST树
# with open(r'F:\AAA研究生资料\Replication-master\bluir_python\demo_srouce.py', 'r') as f:
#     source_code = f.read()
#     tree = ast.parse(source_code)
#     visitor = IdentifierVisitor()
#     visitor.generic_visit(tree)
#     # 输出找到的所有id
#     for id in visitor.items:
#         # print(transform(id))
#         print(id)

# str = 'URL in readme (https://2.python-requests.org/) is http only'
# print(transform(str))

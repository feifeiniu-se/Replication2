import ast
import os
import re
import textwrap
from node_visitors import ClassVisitor, FuncVisitor, IdentifierVisitor, transform

# 定义函数,用于获取Python文件的单行注释,find single_line comments
def findsl_comments(code):
    # 用正则表达式定义字符串匹配的模式pattern，或者说规则
    pattern = '# (.*)'
    comments = re.findall(pattern, code)
    return comments


# 定义函数,用于获取Python文件的多行注释
def findml_comments(code):
    pattern = re.compile('(?:""")(.*?)(?:""")', re.DOTALL)
    comments = pattern.findall(code)
    return comments

pyfiles = []
def findpy(obj):
    if obj.endswith(".py"):  # endswith()  判断以什么什么结尾
        print(obj)

# 遍历文件夹找到指定py后缀结尾的文件
def list_allfile(dir_path):
    dir_files = os.listdir(dir_path)  # 得到该文件夹下所有的文件
    for file in dir_files:
        file_path = os.path.join(dir_path, file)  # 路径拼接成绝对路径
        if os.path.isfile(file_path):  # 如果是文件，就打印这个文件路径
            if file_path.endswith(".py"):
                pyfiles.append(file_path)
        if os.path.isdir(file_path):  # 如果目录，就递归子目录
            list_allfile(file_path)
    return pyfiles



path = "F:\Python_dataset"
path_dir = "F:\Python_dir"
files = os.listdir(path)
files = ["certbot", "compose", "django_rest_framework", "flask", "keras", "mitmproxy", "pipenv", "requests","scrapy","scikit-learn", "spaCy", "tornado"]
files = ["django_rest_framework", "flask", "keras", "mitmproxy", "pipenv", "requests","scrapy", "spaCy", "tornado"]
files = ["certbot"]
for file in files[:]:
    print(file, end=" ")
    filePath = path+"\\"+file+"-master"
    dirPath = path_dir+"\\"+file
    # if os.path.exists(dirPath):
    #     os.remove(dirPath)
    os.makedirs(dirPath)
    # 每个py文件的绝对路径
    count = 1
    for absolutePath in list_allfile(filePath):
        # 数据库路径
        path = absolutePath[len(filePath) + 1:]
        f = open(dirPath + "/doc-" + str(count), "w", encoding="ascii")
        f.write("<DOC>\n<DOCNO>" + path.replace('\\', '/') + " </DOCNO>\n<text>\n")

        with open(absolutePath, 'r', encoding='latin') as f2:
            source_code = f2.read()
            tree = ast.parse(source_code)
            visitor_Func = FuncVisitor()
            visitor_Func.visit(tree)
            visitor_Class = ClassVisitor()
            visitor_Class.visit(tree)
            visitor_Id = IdentifierVisitor()
            visitor_Id.visit(tree)

            f.write("<class>\n");
            for cla in visitor_Class.classes:
                f.write(transform(cla))
                f.write("\n")
            f.write("</class>\n");

            f.write("<method>\n");
            for func in visitor_Func.functions:
                f.write(transform(func))
                f.write("\n")
            f.write("</method>\n");

            f.write("<identifier>\n");
            for id in visitor_Id.items:
                if id:
                    f.write(transform(id))
                    f.write("\n")
            f.write("</identifier>\n");

            f.write("<comments>\n");
            # 写注释
            docstring_s = findsl_comments(source_code)
            docstring_m = findml_comments(source_code)
            comp = re.compile('[^A-Z^a-z^0-9^ ]')
            comments_all = ''
            # 遍历，写入Python多行注释
            for i in range(len(docstring_m)):
                comments = comp.sub('', docstring_m[i])
                f.write(transform(comments))
                f.write("\n")
                comments_all += comments
                # print(f'"""{comments}\n"""\n')
            # 遍历，写入Python单行注释
            for i in range(len(docstring_s)):
                comments = comp.sub('', docstring_s[i])
                f.write(transform(comments))
                f.write("\n")
                comments_all += comments
                # print(f"# {comments}\n")
            f.write("</comments>\n");
            f2.close()

        f.write("</text>\n</DOC>\n");
        f.close()
        count += 1

    pyfiles.clear()





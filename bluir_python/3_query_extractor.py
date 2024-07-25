import sqlite3
import re
from xml.etree.ElementTree import Element, SubElement, tostring




def transform(name):
    processed_name = re.sub(
        r'(?<=[A-Z])(?=[A-Z][a-z])|(?<=[^A-Z])(?=[A-Z])|(?<=[A-Za-z])(?=[^A-Za-z])',
        ' ',
        name
    ).lower().split()

    transformed_string = ' '.join([word.strip() for word in processed_name if len(word.strip()) > 2])

    return transformed_string.strip()
def process(query):
    # 使用正则表达式替换非字母数字字符为空格
    query = re.sub(r'[^\w\s]', ' ', query)
    # 分割字符串为单词列表
    words = query.split()

    # 初始化处理后的查询字符串，并遍历单词列表
    processed_query = ""
    for word in words:
        # 调用transform函数（假设只是返回原单词）并添加到结果字符串
        processed_query += " " + transform(word)

        # 去除开头的空格并返回结果
    return processed_query.strip()


def process1(query):
    query = re.sub(r'[^\w\s]', ' ', query)

    words = query.split()

    processed_query = ""
    for word in words:
        if len(word) > 2:
            processed_query += " " + word

    return processed_query.strip()

def addField(str_input, field_name, weight):
    query_parts = str_input.split()
    added_str = " ".join([
        f"{weight} {part}.({field_name})" if part else ""
        for part in query_parts
    ])
    return added_str.strip()

class BugReport:
    def __init__(self, id, summary, description, *args):
        self.id = id
        self.summary = summary
        self.description = description

    def getBugId(self):
        return self.id

    def getSummary(self):
        return self.summary

    def getDescription(self):
        return self.description



def extractSumDesField(project):
    outputPath = "F:\\Python_query\\" + project +"\\query"
    sql = "SELECT * FROM issue"
    bug_reports = []
    url = 'F:/AAA研究生资料/dataset/' + project +'.sqlite3'

    try:
        conn = sqlite3.connect(url)
        cursor = conn.cursor()
        cursor.execute(sql)

        for res in cursor.fetchall():
            bug_reports.append(BugReport(res[0], res[2], res[3]))

    except sqlite3.Error as e:
        print(e)

    with open(outputPath, 'w') as file:
        file.write("<parameters>\n")

        for bug in bug_reports:
            file.write("\t<query>\n")
            file.write(f"\t\t<number>{bug.getBugId()}</number>\n")

            summary_processed = process(bug.getSummary())
            summary_processed1 = process1(bug.getSummary())
            description_processed = process(bug.getDescription())
            description_processed1 = process1(bug.getDescription())

            # 构建 <text> 标签的内容
            text_content = "#weight("
            text_content += addField(summary_processed, "class", 1.0) + " "
            text_content += addField(summary_processed1, "class", 1.0) + " "
            text_content += addField(description_processed, "class", 1.0) + " "
            text_content += addField(description_processed1, "class", 1.0) + " "

            text_content += addField(summary_processed, "method", 1.0) + " "
            text_content += addField(summary_processed1, "method", 1.0) + " "
            text_content += addField(description_processed, "method", 1.0) + " "
            text_content += addField(description_processed1, "method", 1.0) + " "

            text_content += addField(summary_processed, "identifier", 1.0) + " "
            text_content += addField(summary_processed1, "identifier", 1.0) + " "
            text_content += addField(description_processed, "identifier", 1.0) + " "
            text_content += addField(description_processed1, "identifier", 1.0) + " "

            text_content += addField(summary_processed, "comments", 1.0) + " "
            text_content += addField(description_processed, "comments", 1.0)
            text_content += ")\n"

            file.write(f"\t\t<text>{text_content}</text>\n")
            file.write("\t</query>\n")

        file.write("</parameters>\n")

    return len(bug_reports)


pro = ["compose", "django_rest_framework", "flask", "keras", "pipenv", "requests", "scrapy", "spaCy", "tornado",
        "certbot"]
pro = ["certbot"]
for project in pro:
    extractSumDesField(project)


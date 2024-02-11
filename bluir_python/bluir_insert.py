import sqlite3


def read_indriQueryResult(project):
    # read from index

    path = "F:/Python_result/" + project+"/result.txt"
    re = open(path, encoding='utf-8')
    lines = re.readlines()
    items = []
    for line in lines:
        line = line.replace("\n", "").split(" ")
        item = []
        id = line[0]
        file = line[2]
        score = line[4]
        item.append(id)
        item.append(file)
        item.append(score)
        items.append(item)
    print(items)

    insert_database(project, items)

def insert_database(project, items):
    path = "F:/AAA研究生资料/dataset/" + project+".sqlite3"

    connection = sqlite3.connect(path)
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.execute("drop table if exists Bluir")
    cursor.execute("create table Bluir (issue_id text, file_path text, score text)")
    cursor.executemany("insert into Bluir values(?,?,?)", items)
    connection.commit()
    cursor.close()
    connection.close()




projects = [ "compose", "django_rest_framework", "flask", "keras",  "pipenv", "requests",  "scrapy", "spaCy", "tornado"]
projects = ["mitmproxy"]
for p in projects[:]:
    # path = "F:/AAA研究生资料/dataset/" + p+".sqlite3"
    # print(path)
    # connection = sqlite3.connect(path)
    # connection.text_factory = str
    # cursor = connection.cursor()
    # cursor.execute("update Bluir set file_path = REPLACE(file_path,'\','/') where 1=1")
    # connection.commit()
    # cursor.close()
    # connection.close()
    print(p)
    read_indriQueryResult(p)

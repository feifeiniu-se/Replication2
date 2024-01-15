import sqlite3


def read_indriQueryResult(project):
    # read from index

    path = "C:/Users/Feifei/bluir/BLUiR_" + project+"/"
    index = path + "FileIndex.txt"
    bluir_score = path + "indriQueryResult"
    fIndex = open(index, encoding='utf-8')
    lines = fIndex.readlines()
    mapping = {} # classname filepath
    issue_mapping = {}
    for tmp in lines:
        line = tmp.replace("\n", "").split("\t")
        if line[2] in mapping:
            mapping[line[2]].add(line[1])
        else:
            mapping[line[2]] = set()
            mapping[line[2]].add(line[1])
    # read from indriQueryResult bluir即代码结构分数是直接获取的
    fResult = open(bluir_score, encoding='utf-8')
    lines = fResult.readlines()
    for tmp in lines:
        line = tmp.replace("\n", "").split(" ")
        if line[0] in issue_mapping:
            map = issue_mapping.get(line[0])
            class_set = mapping.get(line[2])
            # print(line[2])
            # print(class_set)
            if class_set is not None:
                for c in class_set:
                    map[c] = line[4]
        else:
            map = {}
            class_set = mapping.get(line[2])
            if class_set is not None:
                for c in class_set:
                    map[c] = line[4]
            issue_mapping[line[0]] = map
    print(len(issue_mapping))
    insert_database(project, issue_mapping)

def insert_database(project, issue_mapping):
    path = "F:\AAA研究生资料\dataset/" + project+".sqlite3"
    data = []
    for issue, files in issue_mapping.items():
        for f,s in files.items():
            x = [issue, f, s]
            data.append(x)

    connection = sqlite3.connect(path)
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.execute("drop table if exists Bluir")
    cursor.execute("create table Bluir (issue_id text, file_path text, score text)")
    cursor.executemany("insert into Bluir values(?,?,?)", data)
    connection.commit()
    cursor.close()
    connection.close()



# projects = ["derby", "drools", "hornetq", "izpack", "keycloak", "log4j2", "railo", "seam2", "teiid", "weld", "wildfly"]
projects = ["lucene", "hive", "hadoop", "hbase", "hive", "hornetq", "infinispan", "izpack", "jbehave", "jboss-transaction-manager", "jbpm", "kafka", "keycloak", "log4j2", "lucene", "maven", "pig", "railo", "resteasy", "seam2", "spark", "switchyard", "teiid", "wildfly", "zookeeper"]
# projects = ["archiva", "axis2", "cassandra", "derby", "drools", "errai", "flink", "groovy", "hadoop", "hbase", "hibernate", "hive", "hornetq", "infinispan", "izpack", "jbehave", "jboss-transaction-manager", "jbpm", "kafka", "keycloak", "log4j2", "lucene", "maven", "pig", "railo", "resteasy", "seam2", "spark", "switchyard", "teiid", "weld", "wildfly", "zookeeper"]
for p in projects[:1]:
    print(p)
    read_indriQueryResult(p)

import os
import re
import sqlite3
import string


path = "F:\AAA研究生资料\dataset"
files = os.listdir(path)
# files = ["archiva", "axis2", "cassandra", "derby", "drools", "errai", "flink", "groovy", "hadoop", "hbase", "hibernate", "hive", "hornetq", "infinispan", "izpack", "jbehave", "jboss-transaction-manager", "jbpm", "kafka", "keycloak", "log4j2", "lucene", "maven", "pig", "railo", "resteasy", "seam2", "spark", "switchyard", "teiid", "weld", "wildfly", "zookeeper"]
files = ["certbot", "compose", "django_rest_framework", "flask", "keras", "mitmproxy", "pipenv", "requests", "scikit-learn", "scrapy", "spaCy", "tornado"]
for file in files[:]:
    print(file, end=" ")
    filePath = path+"\\"+file + ".sqlite3"
    connection = sqlite3.connect(filePath)
    connection.text_factory = str
    cursor = connection.cursor()
    # 创建视图
    # cursor.execute(
    #     "create view v_commit_change_file as select change_set.*, code_change.* from code_change inner join change_set on change_set.fix_id = code_change.fix_id"
    #     )
    cursor.execute(
        "drop table BugCache"
        )
    connection.commit()
    cursor.close()
    connection.close()
    print()
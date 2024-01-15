import os

from replication.read import read_issues
from tracescore.tracescore import calculate

path = "F:\AAA研究生资料\dataset"
files = os.listdir(path)
# files = ["archiva", "axis2", "cassandra", "derby", "drools", "errai", "flink", "groovy", "hadoop", "hbase", "hibernate", "hive", "hornetq", "infinispan", "izpack", "jbehave", "jboss-transaction-manager", "jbpm", "kafka", "keycloak", "log4j2", "lucene", "maven", "pig", "railo", "resteasy", "seam2", "spark", "switchyard", "teiid", "weld", "wildfly", "zookeeper"]
files = ["archiva", "cassandra", "errai", "flink", "groovy", "hbase", "hibernate", "hive", "jboss-transaction-manager", "kafka", "lucene", "maven", "resteasy", "spark", "switchyard", "zookeeper"]
# "jbehave", "jbpm"

for file in files[:]:
    print(file, end=" ")
    filePath = path+"\\"+file + ".sqlite3"
    issues = read_issues(filePath)
    issues = [issue for issue in issues if len(issue.files)>0]

    calculate(issues, filePath)
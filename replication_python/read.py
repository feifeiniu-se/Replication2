# read issues from sqlite python
import sqlite3
import datetime

from sklearn.feature_extraction.text import TfidfVectorizer

from replication_python.File_tracescore import File_tracescore
from data_processing.Issue import Issue
from tracescore.File_issues import File_issues

# python
def read_issues(path):
    issue_map = {}
    connection = sqlite3.connect(path)
    connection.text_factory = str
    cursor = connection.cursor()
    # 修改过的bug报告
    cursor.execute("select issue_id, type, resolved_date, summary_stem, description_stem, created_date from issue where resolved_date is not null and issue_id in (select issue_id from change_set_link) order by resolved_date")
    result = cursor.fetchall()

    issues, texts = [], []
    for tmp in result:
        new_issue = Issue(tmp)
        issues.append(new_issue)
        issue_map[new_issue.issue_id] = new_issue

    #tfidf
    texts = [x.summary_stem + " " + x.description_stem for x in issues]
    vectorizer = TfidfVectorizer(encoding='utf-8')
    vectorizer.fit(texts)
    # 计算每个bug报告的Tf-Idf，得到特征向量
    for issue in issues:
        issue.tfidf = vectorizer.transform([issue.summary_stem + " " + issue.description_stem]).toarray()[0:1]

    # read files
    cursor.execute("select issue_id, fix_id, file_path, fix_date from v_code_change")

    result = cursor.fetchall()
    for tmp in result:
        issue = issue_map[tmp[0]]
        issue.files.append(File_tracescore(tmp))
        # time of first commit, and first commit hash
        if datetime.datetime.strptime(str(issue.first_commit_date), "%Y-%m-%d %H:%M:%S") > datetime.datetime.strptime(tmp[3].replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S"):
            issue.first_commit_date = datetime.datetime.strptime(tmp[3].replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S")
            issue.first_commit_hash = set()
            issue.first_commit_hash.add(tmp[1])
        if datetime.datetime.strptime(str(issue.first_commit_date), "%Y-%m-%d %H:%M:%S") == datetime.datetime.strptime(tmp[3].replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S"):
            issue.first_commit_hash.add(tmp[1])

    # # read source files for each commit #todo
    # # source code list
    # map_file = {} # commit_hash, source code files
    # connection.text_factory = str
    # cursor = connection.cursor()
    # cursor.execute("select * from Commit_files_link")
    # result = cursor.fetchall()
    # for tmp in result:
    #     map_file[tmp[0]] = tmp[1]
    #
    # for issue in issues:
    #     if issue.issue_type=='Bug':
    #         for hash in issue.first_commit_hash:
    #             files = map_file[hash].replace("[","").replace("]","").split(", ")
    #             issue.source_files.update(tuple(files))
    #
    # cursor.close()
    # connection.close()

    return issues


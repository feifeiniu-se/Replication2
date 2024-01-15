# read issues from sqlite
import sqlite3
import datetime

from sklearn.feature_extraction.text import TfidfVectorizer

from data_processing.File_tracescore import File_tracescore
from data_processing.Issue import Issue
from tracescore.File_issues import File_issues


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
    texts = [x.summary_stem + " " + x.description_stem for x in issues if x.issue_type == "Bug"]
    vectorizer = TfidfVectorizer(encoding='utf-8')
    vectorizer.fit(texts)
    # 计算每个bug报告的Tf-Idf，得到特征向量
    for issue in issues:
        issue.tfidf = vectorizer.transform([issue.summary_stem + " " + issue.description_stem]).toarray()[0:1]

    # read ground truth
    cursor.execute("select issue_id, commit_hash, committed_date, file_path, old_file_path, change_type, is_deleted, sum_added_lines, sum_removed_lines from v_code_change where file_path like '%.java' and issue_id in (select issue_id from issue where resolved_date is not null)")
    result = cursor.fetchall()
    for tmp in result:
        issue = issue_map[tmp[0]]
        x = File_issues(tmp)
        # 每个bug报告修改涉及的源文件
        issue.files.append(File_issues(tmp))

        # update time of first commit, and first commit hash
        if datetime.datetime.strptime(str(issue.first_commit_date), "%Y-%m-%d %H:%M:%S") > datetime.datetime.strptime(tmp[2].replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S"):
            issue.first_commit_date = datetime.datetime.strptime(tmp[2].replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S")
            issue.first_commit_hash = set()
            issue.first_commit_hash.add(tmp[1])
        if datetime.datetime.strptime(str(issue.first_commit_date), "%Y-%m-%d %H:%M:%S") == datetime.datetime.strptime(tmp[2].replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S"):
            issue.first_commit_hash.add(tmp[1])

    # read source files for each commit #todo
    # source code list
    map_file = {} # commit_hash, source code files
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.execute("select * from Commit_files_link")
    result = cursor.fetchall()
    for tmp in result:
        map_file[tmp[0]] = tmp[1]

    for issue in issues:
        if issue.issue_type=='Bug':
            for hash in issue.first_commit_hash:
                files = map_file[hash].replace("[","").replace("]","").split(", ")
                issue.source_files.update(tuple(files))

    cursor.close()
    connection.close()

    return issues


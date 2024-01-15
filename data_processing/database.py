# -*- coding:utf-8 -*-
import os
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
import datetime

from data_processing.File_tracescore import File_tracescore
from data_processing.Issue import Issue



def read_text_sqlite(issues, path):
    issue_map = {}
    connection = sqlite3.connect(path)
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.execute("select issue_id, summary, description from issue")
    result = cursor.fetchall()
    for tmp in result:
        issue_map[tmp[0]] = tmp

    for issue in issues:
        issue.summary = issue_map[issue.issue_id][1]
        issue.description = issue_map[issue.issue_id][2]
    return issues


def insert_database_tracescore(path, bugs):
    data = []
    for bug in bugs:
        if len(bug.simi_score)>0:
            for f in bug.simi_score:
                x = [bug.issue_id, f, bug.simi_score[f]]
                data.append(x)

    connection = sqlite3.connect(path)
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.execute("drop table if exists TraceScore")
    cursor.execute("create table TraceScore (issue_id text, file_path text, score text)")
    cursor.executemany("insert into TraceScore values(?,?,?)", data)
    connection.commit()
    cursor.close()
    connection.close()

#load bluir, cache, simi score
def read_scores(path, issues):

    issue_map = {issue.issue_id:issue for issue in issues}

    connection = sqlite3.connect(path)
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.execute("select * from Bluir")
    result = cursor.fetchall()
    for tmp in result:
        if tmp[0] in issue_map:
            issue = issue_map[tmp[0]]
            issue.bluir_score[tmp[1]] = float(tmp[2])

    cursor.execute("select * from TraceScore")
    result = cursor.fetchall()
    for tmp in result:
        if tmp[0] in issue_map:
            issue = issue_map[tmp[0]]
            issue.simi_score[tmp[1]] = float(tmp[2])

    cursor.execute("select * from Cache")
    result = cursor.fetchall()
    for tmp in result:
        if tmp[0] in issue_map:
            issue = issue_map[tmp[0]]
            if tmp[1] in issue.simi_score or tmp[1] in issue.bluir_score:
                issue.cache_score[tmp[1]] = float(tmp[2])


def read_tracescore(path):
    issue_map = {} # <issue_id, issue>
    connection = sqlite3.connect(path)
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.execute(
        "select issue_id, issue_type, fixed_date, summary_stemmed, description_stemmed, created_date from issue where issue_id in (select issue_id from v_issue_statistic) order by fixed_date")
    result = cursor.fetchall()

    issues, texts = [], []
    for tmp in result:
        new_issue = Issue(tmp)
        issues.append(new_issue)
        issue_map[new_issue.issue_id] = new_issue

    # # tfidf
    texts = [x.summary_stem+" "+x.description_stem for x in issues if x.issue_type=="Bug"]
    vectorizer = TfidfVectorizer(encoding='utf-8')
    vectorizer.fit(texts)
    for issue in issues:
        issue.tfidf = vectorizer.transform([issue.summary_stem + " " + issue.description_stem]).toarray()[0:1]

    # # read files
    cursor.execute("select issue_id, commit_hash, file_path, committed_date from v_code_change")

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

    # source code list
    map_file = {} # commit_hash, source code files
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.execute("select * from Commit_files_link")
    result = cursor.fetchall()
    for tmp in result:
        map_file[tmp[0]] = tmp[1]

    for issue in issues:
        for hash in issue.first_commit_hash:
            files = map_file[hash].replace("[","").replace("]","").split(", ")
            issue.source_files.update(tuple(files))

    # mapping_files = {}# file_name, codeBlockID
    # cursor.execute("select * from Files")
    # result = cursor.fetchall()
    # for tmp in result:
    #     mapping_files[tmp[0]] = tmp[1]

    cursor.close()
    connection.close()

    return issues



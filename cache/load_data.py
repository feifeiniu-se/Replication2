import sqlite3

from cache.Commit import Commit
from data_processing.File_tracescore import File_tracescore
from data_processing.Issue import Issue
import datetime
import numpy as np


def read_commits(path):
    commit_map = {} # <commit_hash, commit>
    connection = sqlite3.connect(path)
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.execute("select commit_hash, committed_date, message, file_path from v_commit_change_file where is_deleted=0 and file_path like '%.java'")
    result = cursor.fetchall()

    for tmp in result:
         # only include commits for bug/fix
        if "merge pull request" in tmp[2].lower(): # exclude merge files
            continue
        if tmp[0] in commit_map:
            commit_map[tmp[0]].files.add(tmp[3])
        else:
            commit_map[tmp[0]] = Commit(tmp)
            commit_map[tmp[0]].files.add(tmp[3])
    return [commit_map[hash] for hash in commit_map]

def insert_database(path, bugs):
    data = []
    for bug in bugs:
        if len(bug.cache_score)>0:
            for f in bug.cache_score:
                x = [bug.issue_id, f, bug.cache_score[f]]
                data.append(x)

    connection = sqlite3.connect(path)
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.execute("drop table if exists Cache")
    cursor.execute("create table Cache (issue_id text, file_path text, score text)")
    cursor.executemany("insert into Cache values(?,?,?)", data)
    connection.commit()
    cursor.close()
    connection.close()

# def insert_database_vector(path, bugs):
#     data = []
#     for bug in bugs:
#         if len(bug.cache_score)>0:
#             for f in bug.cache_score:
#                 x = [bug.issue_id, f, str(bug.cache_score[f])]
#                 data.append(x)
#
#     connection = sqlite3.connect(path)
#     connection.text_factory = str
#     cursor = connection.cursor()
#     cursor.execute("drop table Cache")
#     cursor.execute("drop table Cache_new")
#     cursor.execute("drop table Cache_PM")
#     cursor.execute("create table Cache (issue_id text, file_path text, vector text)")
#     cursor.executemany("insert into Cache values(?,?,?)", data)
#     connection.commit()
#     cursor.close()
#     connection.close()


# def load_issues(path):
#     issue_map = {} # <issue_id, issue>
#     connection = sqlite3.connect(path)
#     connection.text_factory = str
#     cursor = connection.cursor()
#     cursor.execute(
#         "select issue_id, issue_type, fixed_date, summary_stemmed, description_stemmed, created_date from issue where issue_type='Bug' and issue_id in (select issue_id from v_issue_statistic) order by fixed_date")
#     result = cursor.fetchall()
#
#     issues, texts = [], []
#     for tmp in result:
#         new_issue = Issue(tmp)
#         issues.append(new_issue)
#         issue_map[new_issue.issue_id] = new_issue
#
#    cursor.execute("select commit_hash, file_path, last_modify_hash, change_type, codeBlockID, last_modify_date, issue_id, committed_date, commit_hash, new_path, new_codeBlockID from v_code_change_file")
#
#     result = cursor.fetchall()
#     for tmp in result:
#         if tmp[6] in issue_map:
#             issue = issue_map[tmp[6]]
#             issue.files.append(File(tmp))
#
#
#             # 增加第一次commit的时间 以及首次commit的hash
#             if datetime.datetime.strptime(str(issue.first_commit_date), "%Y-%m-%d %H:%M:%S") > datetime.datetime.strptime(tmp[7].replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S"):
#                 issue.first_commit_date = datetime.datetime.strptime(tmp[7].replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S")
#                 issue.first_commit_hash = set()
#                 issue.first_commit_hash.add(tmp[8])
#             if datetime.datetime.strptime(str(issue.first_commit_date), "%Y-%m-%d %H:%M:%S") == datetime.datetime.strptime(tmp[7].replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S"):
#                 issue.first_commit_hash.add(tmp[8])
#
#     issues.sort(key=lambda x: datetime.datetime.strptime(str(x.first_commit_date), "%Y-%m-%d %H:%M:%S")) #根据第一个提交的时间重新排序 todo
#     # print()
#
#
#     # 读取每个commit所对应的source code list
#     map_file = {} # commit_hash, source code files
#     connection.text_factory = str
#     cursor = connection.cursor()
#     cursor.execute("select * from Commit_files_link")
#     result = cursor.fetchall()
#     for tmp in result:
#         map_file[tmp[0]] = tmp[1]
#
#     # 此处设置source code为首次提交的commit的source code，注意首次提交的可能不止一个，可能有多个commit，有相同的commit_date
#     for issue in issues:
#         for hash in issue.first_commit_hash:
#             files = map_file[hash].replace("[","").replace("]","").split(", ")
#             issue.source_files.update(tuple(files))
#
#
#     mapping_files = {}# file_name, codeBlockID
#     cursor.execute("select * from Files")
#     result = cursor.fetchall()
#     for tmp in result:
#         mapping_files[tmp[0]] = tmp[1]
#
#     # 更新issue.source_files_ID
#     for issue in issues:
#         issue.source_files_ID = set([mapping_files.get(f) for f in issue.source_files])
#
#
#     # 读取cache和bluir的结果
#     connection.text_factory = str
#     cursor = connection.cursor()
#     cursor.execute("select * from Cache where issue_id in (select issue_id from v_issue_statistic where issue_type='Bug')")
#     result = cursor.fetchall()
#     for tmp in result:
#         issue = issue_map[tmp[0]]
#         issue.cache_score[tmp[1]] = float(tmp[2])
#         # print(tmp)
#         if tmp[1] in mapping_files:
#             file_id = mapping_files[tmp[1]]
#             if file_id in issue.cache_id_score:
#                 issue.cache_id_score[file_id] = issue.cache_id_score[file_id] +  float(tmp[2])
#             else:
#                 issue.cache_id_score[file_id] = float(tmp[2])
#
#     cursor.execute("select * from Cache_new where issue_id in (select issue_id from v_issue_statistic where issue_type='Bug')")
#     result = cursor.fetchall()
#     for tmp in result:
#         issue = issue_map[tmp[0]]
#         issue.cache_score_new[tmp[1]] = [int(x) for x in tmp[2].replace("[", "").replace("]", "").split(", ")]
#         if tmp[1] in mapping_files:
#             file_id = mapping_files[tmp[1]]
#             if file_id in issue.cache_id_score_new:
#                 issue.cache_id_score_new[file_id] = np.array(issue.cache_id_score_new[file_id]) + np.array([int(x) for x in tmp[2].replace("[", "").replace("]", "").split(", ")])
#             else:
#                 issue.cache_id_score_new[file_id] = [int(x) for x in tmp[2].replace("[", "").replace("]", "").split(", ")]
#
#     connection.text_factory = str
#     cursor = connection.cursor()
#     result = ''
#     cursor.execute("select * from Bluir where issue_id in (select issue_id from v_issue_statistic where issue_type='Bug')")
#     result = cursor.fetchall()
#     for tmp in result:
#         issue = issue_map[tmp[0]]
#         issue.bluir_score[tmp[1]] = float(tmp[2])
#         if mapping_files[tmp[1]] in issue.bluir_id_score:
#             issue.bluir_id_score[mapping_files[tmp[1]]] = max(float(tmp[2]), issue.bluir_id_score[mapping_files[tmp[1]]])
#         else:
#             issue.bluir_id_score[mapping_files[tmp[1]]] = float(tmp[2])
#
#     cursor.execute("select * from SimiScore where issue_id in (select issue_id from v_issue_statistic where issue_type='Bug')")
#     result = cursor.fetchall()
#     for tmp in result:
#         issue = issue_map[tmp[0]]
#         issue.simi_id_score[tmp[1]] = float(tmp[2])
#
#     cursor.close()
#     connection.close()
#
#     return issues

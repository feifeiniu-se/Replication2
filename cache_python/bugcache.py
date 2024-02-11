import datetime
import math
import os
import sqlite3

from cache_python.load_data import read_commits, insert_database
from data_processing.database import read_tracescore
from evaluation.evaluation import evaluation
import numpy as np

from replication_python.read import read_issues


def loadFileCommitHistory(commits):
    commits.sort(key=lambda x:x.commit_date)
    fileHistories = {}
    for commit in commits:
        for f in commit.files:
            if f in fileHistories:
                fileHistories.get(f).append(commit)
            else:
                fileHistories[f] = []
                fileHistories[f].append(commit)
    return fileHistories

def isBugFixing(message, bugids):
    message = message.lower()
    if "fix" in message or "bug" in message:
        return True
    result = [id for id in bugids if id.lower() in message]
    if len(result)>0:
        return True
    return False

def versionHistoryCompute(issues, fileHistories, days):
    for bug in issues:
        end_date = bug.first_commit_date #todo
        start_date = end_date - datetime.timedelta(days=days)
        rangeTime = days*24*60
        file_score = {} # filePath:score
        for f,v in fileHistories.items():
            v.sort(key=lambda x: x.commit_date)
            v = [commit for commit in v if commit.commit_date<end_date and commit.commit_date>start_date]
            # v = [commit for commit in v if isBugFixing(commit.message, bugids) and commit.commit_date<end_date and commit.commit_date>start_date]
            if len(v)>0:
                score = 0.0
                for commit in v:
                    normalized_t = float((commit.commit_date-start_date).total_seconds()/60) / rangeTime
                    # print(normalized_t)
                    score = score + float(1/(1+np.exp(-12*normalized_t+12)))
                if score>0.0:
                    file_score[f] = score
        bug.cache_score = file_score

def calculate(bugs):
    print(len(bugs), end=";")
    train_size = int(len(bugs) * 0.8)
    test_bugs = bugs[train_size:]

    for issue in test_bugs:
        sorted_files2 = sorted(issue.cache_score.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.predict_bf = [x[0] for x in sorted_files2]
        # issue.predict_bf = [x[0] for x in sorted_files2 if x[0] in issue.source_files] # todo

    ground_truth = [set(f.new_filePath for f in issue.files if f.new_filePath != "/dev/null" and f.new_filePath is not None) for issue in test_bugs]
    predict_result = [issue.predict_bf for issue in test_bugs]

    evaluation(ground_truth, predict_result)


# python dataset issues
path = "F:\AAA研究生资料\dataset"
files = ["certbot", "compose", "django_rest_framework", "flask", "keras", "mitmproxy", "pipenv", "requests", "scikit-learn", "scrapy", "spaCy", "tornado"]
print(";MAP;MRR;Top 1;Top 5;Top 10")
for file in files[:]:
    print(file, end=" ")
    filePath = path+"\\"+file + ".sqlite3"
    issues = read_issues(filePath)
    issues = [issue for issue in issues if len(issue.files)>0]
    # print(len(issues))
    commits = read_commits(filePath)
    # bugids = [issue.issue_id for issue in issues]
    # commits = [commit for commit in commits if isBugFixing(commit.message, bugids)] # only select bug-fixing commits
    file_history = loadFileCommitHistory(commits) # {filePath: file commit history}
    versionHistoryCompute(issues, file_history, 15)
    insert_database(filePath, issues) #insert cache score into database
    calculate(issues)

import os
import random
from scipy import spatial
from ablots.classifier import DT
from data_processing.database import read_tracescore, read_scores
from evaluation.evaluation import evaluation
from replication_python.read import read_issues
from sklearn.preprocessing import MinMaxScaler

PM = True
# todo
if PM == True:
    big_bug_req_filter = True
    whole_history = False
else:
    big_bug_req_filter = False
    whole_history = True


def evaluate(test):
    ground_truth = [set(f.new_filePath for f in issue.files if f.new_filePath != "/dev/null" and f.new_filePath is not None) for issue in test]

    predict_result = [issue.ablots for issue in test]
    evaluation(ground_truth, predict_result)

def evaluate3_python(issues, flag):
    bugReport = [x for x in issues]
    print(len(bugReport), end=";")
    train_size = int(len(bugReport) * 0.8)

    bugReport.sort(key=lambda x: x.fixed_date)
    test = bugReport[train_size:]


    ground_truth = [set(f.new_filePath for f in issue.files if f.new_filePath != "/dev/null" and f.new_filePath is not None) for issue in test]
    for issue in test:
        if flag == "cache":
            predict = issue.cache_score
        elif flag == "bluir":
            predict = issue.bluir_score
        elif flag == "tracescore":
            predict = issue.simi_score
        sorted_files = sorted(predict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.predict_bf = [x[0] for x in sorted_files]
    predict_result = [issue.predict_bf for issue in test]
    evaluation(ground_truth, predict_result)


def reRank(test, pairs_test, result):
    test_mapping = {issue.issue_id: issue for issue in test}
    for i in range(len(pairs_test)):
        tmp = pairs_test[i]
        issue = test_mapping.get(tmp[0])
        issue.ablots_score[tmp[1]] = result[i]
    for issue in test:
        predict = issue.ablots_score
        sorted_files = sorted(predict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.ablots = [x[0] for x in sorted_files]


def make_pairs(issues):
    pairs = []
    for issue in issues:
        ground_truth = set(f.new_filePath for f in issue.files if f.new_filePath != "/dev/null" and f.new_filePath is not None)
        # 候选源文件列表
        file_candidate = []
        file_candidate.extend([f for f in issue.bluir_score])
        file_candidate.extend([f for f in issue.simi_score])
        file_candidate = set(file_candidate)
        for f in file_candidate:
            value = []
            value.append(issue.issue_id)
            value.append(f)
            value.append(issue.cache_score[f] if f in issue.cache_score else 0)
            value.append(issue.bluir_score[f] if f in issue.bluir_score else 0)
            value.append(issue.simi_score[f] if f in issue.simi_score else 0)
            if f in ground_truth:
                value.append(1)
            else:
                value.append(-1)
            # if (value[2]+value[3]+value[4])>0.5:
            pairs.append(value)

    return pairs


# 使用决策树
def calculate(issues):
    bugReport = [x for x in issues]
    print(len(bugReport), end=";")
    train_size = int(len(bugReport) * 0.8)

    bugReport.sort(key=lambda x: x.fixed_date)
    # 测试集为修改时间后20 % 的bug报告
    test = bugReport[train_size:]
    train = bugReport[:train_size]


    # issue和可能源文件对应的3个分数，以及是否是真的被修改
    pairs_train = make_pairs(train)
    pairs_test = make_pairs(test)

    # DT
    result = DT(pairs_train, pairs_test)
    reRank(test, pairs_test, result)
    evaluate(test)

# 基于偏差+CombSUM
def calculate_bias(issues):
    bugReport = [x for x in issues]
    print(len(bugReport), end=";")
    train_size = int(len(bugReport) * 0.8)

    bugReport.sort(key=lambda x: x.fixed_date)
    test = bugReport[train_size:]

    for issue in test:
        amalgam_score = {}
        file_candidate = []

        file_candidate.extend([f for f in issue.bluir_score])
        file_candidate.extend([f for f in issue.simi_score])
        file_candidate = set(file_candidate)
        dict_all = {}
        dict_cache = {}
        dict_bluir = {}
        dict_simi = {}
        Len = int(len(file_candidate) * 0.1)

        ordered_cache_score = sorted(issue.cache_score.items(), key=lambda x: x[1], reverse=True)
        ordered_bluir_score = sorted(issue.bluir_score.items(), key=lambda x: x[1], reverse=True)
        ordered_simi_score = sorted(issue.simi_score.items(), key=lambda x: x[1], reverse=True)

        cache_candidate = [x[0] for x in ordered_cache_score][:Len]
        cache_candidate = set(cache_candidate)
        bluir_candidate = [x[0] for x in ordered_bluir_score][:Len]
        bluir_candidate = set(bluir_candidate)
        simi_candidate = [x[0] for x in ordered_simi_score][:Len]
        simi_candidate = set(simi_candidate)

        union_candidate = cache_candidate.union(bluir_candidate).union(simi_candidate)

        for f in union_candidate:
            dict_all[f] = 0
            dict_cache[f] = 0
            dict_bluir[f] = 0
            dict_simi[f] = 0

        for f in cache_candidate:
            dict_cache[f] = 1
            dict_all[f] += 1
        for f in bluir_candidate:
            dict_bluir[f] = 1
            dict_all[f] += 1
        for f in simi_candidate:
            dict_simi[f] = 1
            dict_all[f] += 1

        vec_cache = list(dict_cache.values())
        vec_bluir = list(dict_bluir.values())
        vec_simi = list(dict_simi.values())
        vec_all = list(dict_all.values())
        # 余弦相似度
        all_zero = True
        for i in vec_cache:
            if i != 0:
                all_zero = False
                break
        cos_sim_cache = 0
        if all_zero:
            pass
        else:
            cos_sim_cache = 1 - spatial.distance.cosine(vec_cache, vec_all)

        # cos_sim_cache = 1 - spatial.distance.cosine(vec_cache, vec_all)

        all_zero1 = True
        for i in vec_bluir:
            if i != 0:
                all_zero1 = False
                break
        cos_sim_bluir = 0
        if all_zero1:
            pass
        else:
            cos_sim_bluir = 1 - spatial.distance.cosine(vec_bluir, vec_all)
        # cos_sim_bluir = 1 - spatial.distance.cosine(vec_bluir, vec_all)

        all_zero = True
        for i in vec_simi:
            if i != 0:
                all_zero = False
                break
        cos_sim_simi = 0
        if all_zero:
            pass
        else:
            cos_sim_simi = 1 - spatial.distance.cosine(vec_simi, vec_all)
        # cos_sim_simi = 1 - spatial.distance.cosine(vec_simi, vec_all)
        # print('cos_sim_cache:', cos_sim_cache, 'cos_sim_bluir:', cos_sim_bluir, 'cos_sim_simi:', cos_sim_simi)
        # cos_sim_bluir = 1

        for f in file_candidate:
            cache_score = issue.cache_score[f] if f in issue.cache_score else 0
            bluir_score = issue.bluir_score[f] if f in issue.bluir_score else 0
            simi_score = issue.simi_score[f] if f in issue.simi_score else 0
            score = 0

            if cos_sim_bluir <= cos_sim_simi and cos_sim_bluir <= cos_sim_cache:
                # print('simi_score + cache_score')
                score = simi_score + cache_score
                if simi_score != 0 and cache_score != 0:
                    score = score * 2

            if cos_sim_simi <= cos_sim_bluir and cos_sim_simi <= cos_sim_cache:
                # print('bluir_score + cache_score')
                score = bluir_score + cache_score
                if bluir_score != 0 and cache_score != 0:
                    score = score * 2

            if cos_sim_cache <= cos_sim_bluir and cos_sim_cache <= cos_sim_simi:
                # print('bluir_score + simi_score')
                # CombSUM
                score = bluir_score + simi_score
                if bluir_score != 0 and simi_score != 0:
                    score = score * 2
                # score = simi_score * cos_sim_simi + bluir_score * cos_sim_bluir + cache_score * cos_sim_cache
            amalgam_score[f] = score
        sorted_files = sorted(amalgam_score.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        # 每个测试集bug报告的源文件分数排序结果
        issue.ablots = [x[0] for x in sorted_files]


    evaluate(test)


def calculate_fixed(issues):
    bugReport = [x for x in issues]
    print(len(bugReport), end=";")
    train_size = int(len(bugReport) * 0.8)

    bugReport.sort(key=lambda x: x.fixed_date)
    test = bugReport[train_size:]

    for issue in test:
        amalgam_score = {}
        file_candidate = []
        file_candidate.extend([f for f in issue.bluir_score])
        file_candidate.extend([f for f in issue.simi_score])
        file_candidate = set(file_candidate)
        Len = int(len(file_candidate) * 0.1)

        # list
        ordered_cache_score = sorted(issue.cache_score.items(), key=lambda x: x[1], reverse=True)
        ordered_bluir_score = sorted(issue.bluir_score.items(), key=lambda x: x[1], reverse=True)
        ordered_simi_score = sorted(issue.simi_score.items(), key=lambda x: x[1], reverse=True)

        cache_candidate = [x[0] for x in ordered_cache_score][:Len]
        cache_candidate = set(cache_candidate)
        bluir_candidate = [x[0] for x in ordered_bluir_score][:Len]
        bluir_candidate = set(bluir_candidate)
        simi_candidate = [x[0] for x in ordered_simi_score][:Len]
        simi_candidate = set(simi_candidate)
        # print(len(cache_candidate), len(bluir_candidate), len(simi_candidate))
        intersection_cache = cache_candidate.intersection(bluir_candidate.union(simi_candidate))
        intersection_bluir = bluir_candidate.intersection(simi_candidate.union(cache_candidate))
        intersection_simi = simi_candidate.intersection(bluir_candidate.union(cache_candidate))
        # print(len(intersection_cache), len(intersection_bluir), len(intersection_simi))

        for f in file_candidate:
            cache_score = issue.cache_score[f] if f in issue.cache_score else 0
            bluir_score = issue.bluir_score[f] if f in issue.bluir_score else 0
            simi_score = issue.simi_score[f] if f in issue.simi_score else 0

            score = (0.2 * simi_score + 0.8 * bluir_score) * 0.7 + cache_score * 0.3
            # if len(intersection_bluir) <= len(intersection_simi) and len(intersection_bluir) <= len(intersection_cache):
            #     # print('simi_score + cache_score')
            #     score = simi_score + cache_score
            #     # if simi_score != 0 and cache_score != 0:
            #     #     score = score / 2
            #
            # if len(intersection_simi) <= len(intersection_bluir) and len(intersection_simi) <= len(intersection_cache):
            #     # print('bluir_score + cache_score')
            #     score = bluir_score + cache_score
            #     # if bluir_score != 0 and cache_score != 0:
            #     #     score = score / 2
            #
            # if len(intersection_cache) <= len(intersection_bluir) and len(intersection_cache) <= len(intersection_simi):
            #     # print('bluir_score + simi_score')
            #     # CombSUM
            #     score = bluir_score + simi_score
            #     # if bluir_score != 0 and simi_score != 0:
            #     #     score = score / 2

            amalgam_score[f] = score
        sorted_files = sorted(amalgam_score.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        # 每个测试集bug报告的源文件分数排序结果
        issue.ablots = [x[0] for x in sorted_files]


    evaluate(test)


def calculate_corr(issues):
    bugReport = [x for x in issues]
    print(len(bugReport), end=";")
    train_size = int(len(bugReport) * 0.8)

    bugReport.sort(key=lambda x: x.fixed_date)
    test = bugReport[train_size:]

    for issue in test:
        amalgam_score = {}
        file_candidate = []

        file_candidate.extend([f for f in issue.bluir_score])
        file_candidate.extend([f for f in issue.simi_score])
        file_candidate = set(file_candidate)
        dict_all = {}
        dict_cache = {}
        dict_bluir = {}
        dict_simi = {}
        Len = int(len(file_candidate) * 0.1)

        ordered_cache_score = sorted(issue.cache_score.items(), key=lambda x: x[1], reverse=True)
        ordered_bluir_score = sorted(issue.bluir_score.items(), key=lambda x: x[1], reverse=True)
        ordered_simi_score = sorted(issue.simi_score.items(), key=lambda x: x[1], reverse=True)

        cache_candidate = [x[0] for x in ordered_cache_score][:Len]
        cache_candidate = set(cache_candidate)
        bluir_candidate = [x[0] for x in ordered_bluir_score][:Len]
        bluir_candidate = set(bluir_candidate)
        simi_candidate = [x[0] for x in ordered_simi_score][:Len]
        simi_candidate = set(simi_candidate)

        union_candidate = cache_candidate.union(bluir_candidate).union(simi_candidate)

        for f in union_candidate:
            dict_all[f] = 0
            dict_cache[f] = 0
            dict_bluir[f] = 0
            dict_simi[f] = 0

        for f in cache_candidate:
            dict_cache[f] = 1
            dict_all[f] += 1
        for f in bluir_candidate:
            dict_bluir[f] = 1
            dict_all[f] += 1
        for f in simi_candidate:
            dict_simi[f] = 1
            dict_all[f] += 1

        vec_cache = list(dict_cache.values())
        vec_bluir = list(dict_bluir.values())
        vec_simi = list(dict_simi.values())
        vec_all = list(dict_all.values())
        list_simi = 0
        for i in range(len(vec_simi)):
            if vec_simi[i] == 1:
                list_simi += vec_all[i]
        list_bluir = 0
        for i in range(len(vec_bluir)):
            if vec_bluir[i] == 1:
                list_bluir += vec_all[i]
        list_cache = 0
        for i in range(len(vec_cache)):
            if vec_cache[i] == 1:
                list_cache += vec_all[i]


        w_bluir = 0
        w_cache = 0
        w_simi = 0
        if len(simi_candidate) == 0:
            pass
        else:
            w_simi = 1 - (list_simi - len(simi_candidate)) / (len(simi_candidate) * len(union_candidate))
        if len(bluir_candidate) == 0:
            pass
        else:
            w_bluir = 1 - (list_bluir - len(bluir_candidate)) / (len(bluir_candidate) * len(union_candidate))
        if len(cache_candidate) == 0:
            pass
        else:
            w_cache = 1 - (list_cache - len(cache_candidate)) / (len(cache_candidate) * len(union_candidate))


        for f in file_candidate:
            cache_score = issue.cache_score[f] if f in issue.cache_score else 0
            bluir_score = issue.bluir_score[f] if f in issue.bluir_score else 0
            simi_score = issue.simi_score[f] if f in issue.simi_score else 0
            score = simi_score * w_simi + bluir_score * w_bluir + cache_score * w_cache
            amalgam_score[f] = score
        sorted_files = sorted(amalgam_score.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        # 每个测试集bug报告的源文件分数排序结果
        issue.ablots = [x[0] for x in sorted_files]


    evaluate(test)

def calculate_borda(issues):
    bugReport = [x for x in issues]
    print(len(bugReport), end=";")
    train_size = int(len(bugReport) * 0.8)

    bugReport.sort(key=lambda x: x.fixed_date)
    test = bugReport[train_size:]

    for issue in test:
        amalgam_score = {}
        file_candidate = []
        file_candidate.extend([f for f in issue.bluir_score])
        file_candidate.extend([f for f in issue.simi_score])
        file_candidate = set(file_candidate)
        Len = int(len(file_candidate) * 0.1)

        ordered_cache_score = sorted(issue.cache_score.items(), key=lambda x: x[1], reverse=True)
        ordered_cache_score = [x[0] for x in ordered_cache_score]
        ordered_bluir_score = sorted(issue.bluir_score.items(), key=lambda x: x[1], reverse=True)
        ordered_bluir_score = [x[0] for x in ordered_bluir_score]
        ordered_simi_score = sorted(issue.simi_score.items(), key=lambda x: x[1], reverse=True)
        ordered_simi_score = [x[0] for x in ordered_simi_score]

        cache_candidate = [x[0] for x in ordered_cache_score][:Len]
        cache_candidate = set(cache_candidate)
        bluir_candidate = [x[0] for x in ordered_bluir_score][:Len]
        bluir_candidate = set(bluir_candidate)
        simi_candidate = [x[0] for x in ordered_simi_score][:Len]
        simi_candidate = set(simi_candidate)
        # print(len(cache_candidate), len(bluir_candidate), len(simi_candidate))
        intersection_cache = cache_candidate.intersection(bluir_candidate.union(simi_candidate))
        intersection_bluir = bluir_candidate.intersection(cache_candidate.union(simi_candidate))
        intersection_simi = simi_candidate.intersection(bluir_candidate.union(cache_candidate))
        # print(len(intersection_cache), len(intersection_bluir), len(intersection_simi))

        Len = len(file_candidate)

        for f in file_candidate:
            cache_score = Len - ordered_cache_score.index(f) if f in ordered_cache_score else 0
            bluir_score = Len - ordered_bluir_score.index(f) if f in ordered_bluir_score else 0
            simi_score = Len - ordered_simi_score.index(f) if f in ordered_simi_score else 0

            if len(intersection_bluir) <= len(intersection_simi) and len(intersection_bluir) <= len(intersection_cache):
                score = simi_score + cache_score

            if len(intersection_simi) <= len(intersection_bluir) and len(intersection_simi) <= len(intersection_cache):
                score = bluir_score + cache_score

            if len(intersection_cache) <= len(intersection_bluir) and len(intersection_cache) <= len(intersection_simi):
                score = bluir_score + simi_score

            amalgam_score[f] = score
        sorted_files = sorted(amalgam_score.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        # 每个测试集bug报告的源文件分数排序结果
        issue.ablots = [x[0] for x in sorted_files]


    evaluate(test)
# python dataset *
path = "F:\AAA研究生资料\dataset"
files = os.listdir(path)
files = ["certbot", "compose", "django_rest_framework", "flask", "keras", "mitmproxy", "pipenv", "requests", "scikit-learn", "scrapy", "spaCy", "tornado"]
# files = ["mitmproxy"]
print(";MAP;MRR;Top 1;Top 5;Top 10")
for file in files[:]:
    print(file, end=" ")
    filePath = path+"\\"+file + ".sqlite3"
    issues = read_issues(filePath)
    read_scores(filePath, issues)
    issues = [issue for issue in issues if len(issue.files) > 0]
    # evaluate3_python(issues, "cache")
    # evaluate3_python(issues, "tracescore")
    # evaluate3_python(issues, "bluir")
    # calculate(issues)
    calculate_fixed(issues)
    # calculate_bias(issues)
    # calculate_corr(issues)
    # calculate_borda(issues)
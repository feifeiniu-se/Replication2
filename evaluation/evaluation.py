def getTopK(k, ground_truth, predicted_result):
    res = 0
    for i in range(len(ground_truth)):
        if (isTopK(k, ground_truth[i], predicted_result[i])):
            res = res + 1
    # print("ok1")
    print("%.3f" % float(res / len(ground_truth)), end=";")


def get_P(k, ground_truth, predicted_result):
    precision = 0.0
    for i in range(len(ground_truth)):
        p = get_precision(k, ground_truth[i], predicted_result[i])
        precision = precision + p
    precision = float(precision / len(ground_truth))
    print("%.3f" % precision, end=";")

def get_R(k, ground_truth, predicted_result):
    recall = 0.0
    for i in range(len(ground_truth)):
        r = get_recall(k, ground_truth[i], predicted_result[i])
        recall = recall + r
    recall = float(recall / len(ground_truth))
    print("%.3f" % recall, end=";")


def getMAP(ground_truth, predicted_result):
    map = 0.0
    for i in range(len(ground_truth)):
        map = map + getAvPrecision(ground_truth[i], predicted_result[i])
    # print("ok3")
    print("%.3f" % float(map / len(ground_truth)), end=";")


def getMRR(ground_truth, predicted_result):
    mrr = 0.0
    for i in range(len(ground_truth)):
        mrr = mrr + getRR(ground_truth[i], predicted_result[i])
    # print("ok4")
    print("%.3f" % float(mrr / len(ground_truth)), end=";")


def isTopK(k, list_gt, list_pr):
    if k< 1:
        k = int(len(list_pr)*k)
    i = 0
    while i < k and i < len(list_pr):
        if list_pr[i] in list_gt:
            return True
        i = i + 1
    return False

def get_precision(t, list_gt, list_pr):
    if t<1:
        t = int(len(list_pr)*t)
    topT = list_pr[:t]
    positive = [x for x in topT if x in list_gt]
    precision = float(len(positive) / t)
    return precision

def get_recall(t, list_gt, list_pr):
    if t<1:
        t = int(len(list_pr)*t)
    topT = list_pr[:t]
    positive = [x for x in topT if x in list_gt]
    recall = len(list_gt) > 0 and float(len(positive) / len(list_gt)) or 0
    return recall


def getAvPrecision(list_gt, list_pr):
    sum = 0.0
    retrived_d = 0
    for i in range(len(list_pr)):
        if list_pr[i] in list_gt:
            retrived_d = retrived_d + 1
            precision_i = float(retrived_d / (i + 1))
            sum = sum + precision_i
    divide = len(list_gt)
    if (divide == 0):
        # print("xx")
        divide = 1
    return sum / divide


def getRR(list_gt, list_pr):
    rr = 0.0
    for i in range(len(list_pr)):
        if list_pr[i] in list_gt:
            rr = float(1 / (i + 1))
            return rr
    return rr

# ground truth 通常指代样本集中的标签
def evaluation(ground_truth, predicted_result):
    # MAP
    getMAP(ground_truth, predicted_result)
    getMRR(ground_truth, predicted_result)
    # topK
    Ks = [1, 5, 10]
    for k in Ks:
        getTopK(k, ground_truth, predicted_result)
    print()

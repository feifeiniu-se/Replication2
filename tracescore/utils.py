from evaluation.evaluation import isTopK
import datetime


def analyze_result(test_bugs):
    # 分析为什么预测对了，为什么没有预测对
    # for analyze
    resY = []
    resN = []
    for issue in test_bugs:
        predict = issue.predict_bf
        gt = set(f.filePath for f in issue.files)
        if(isTopK(10, gt, predict)):
            resY.append(issue)
        else:
            resN.append(issue)
    print()

def last_position(x, pre):
    # x表示的是在pre中的真值，如果x为0，那就返回0
    if(len(x)==0):
        return 0
    else:
        pos = [pre.index(i) for i in x]
        return max(pos)

def time_span_analyze(ground_truth, predict_result, test_bugs):
    gt = 0
    prediction = 0
    # positive = 0
    # pos_gt = 0.0
    # pos_pre = 0.0
    # avg_position = 0.0
    tp_0 = 0
    gt_0 = 0
    # predict_codeBlock = 0.0
    for i in range(len(ground_truth)):
        if len(ground_truth[i])==0:
            gt_0 = gt_0 + 1
            print(test_bugs[i].issue_id)
            continue
        if len(predict_result[i])==0:
            continue
        map_file_days = {}
        for file in test_bugs[i].files:
            map_file_days[file.classBlockID] = (datetime.datetime.strptime(str(file.committed_date).replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(str(file.last_modify_date), "%Y-%m-%d %H:%M:%S")).days
        # print(test_bugs[i].issue_id, end=";")
        print(len(ground_truth[i]), end=";")
        print(len(predict_result[i]), end=";")
        tp = [x for x in ground_truth[i] if x in predict_result[i]]
        print(len(tp), end=";")
        print("%.3f" % float(len(tp)/len(ground_truth[i])), end=";")
        print("%.3f" % float(len(tp)/len(predict_result[i])), end=";")
        # position = last_position(tp, predict_result[i])
        position = [predict_result[i].index(x) for x in tp]
        last_modify = [map_file_days[x] for x in tp]
        print(position, end=";")
        print(last_modify)
        # avg_position = avg_position + int(position)
        gt = gt + len(ground_truth[i])
        prediction = prediction + len(predict_result[i])
        # predict_codeBlock = predict_codeBlock + len(test_bugs[i].predict_bf_r)
        # positive = positive + len(tp)
        # pos_gt = pos_gt + float(len(tp)/len(ground_truth[i]))
        # pos_pre = pos_pre + float(len(tp)/len(predict_result[i]))
        if(len(tp)==0):
            tp_0 = tp_0 + 1

    # print("%.3f" % float(gt/len(ground_truth)), end=";")
    # print("%.3f" % float(prediction/len(ground_truth)), end=";")
    # # print("%.3f" % float(predict_codeBlock / len(ground_truth)), end=";")
    # print("%.3f" % float(positive / len(ground_truth)), end=";")
    # print("%.3f" % float(pos_gt / len(ground_truth)), end=";")
    # print("%.3f" % float(pos_pre / len(ground_truth)), end=";")
    # # print("%.3f" % float(avg_position/len(ground_truth)))
    print("0 gt: "+ str(tp_0) + " " + str(gt_0))
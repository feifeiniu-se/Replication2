# what's the performance of only using cache
import os

from imblearn.under_sampling import RandomUnderSampler
from sklearn.neural_network import MLPClassifier
from sklearn.utils import shuffle
from sklweka.dataset import to_nominal_labels

from cache.load_data import load_issues
from evaluation.evaluation import evaluation

def MLP(train, test):
    x_train = [tmp[2:-1] for tmp in train]
    y_train = [tmp[-1] for tmp in train]
    x_test = [tmp[2:-1] for tmp in test]
    y_test = [tmp[-1] for tmp in test]

    y_train = to_nominal_labels(y_train)
    y_test = to_nominal_labels(y_test)
    rus = RandomUnderSampler(random_state=1)
    # print(x_train[0])
    x_train, y_train = rus.fit_resample(x_train, y_train)
    x_train, y_train = shuffle(x_train, y_train)

    mlp = MLPClassifier(hidden_layer_sizes=(64,16), max_iter=500, random_state=1, solver="adam", activation='logistic') # some projects have the best result tanh(hornetq) logistic(izpack)
    mlp.fit(x_train, y_train)
    y_pred = mlp.predict(x_test)
    prob = mlp.predict_proba(x_test)
    if y_pred[0] == '_bug':
        assert prob[0][0] > prob[0][1]
    if y_pred[0] == '_no_bug':
        assert prob[0][0] < prob[0][1]
    return [k[0] for k in prob]

def make_pairs(issues):
    pairs = []
    for issue in issues:
        ground_truth = set(f.filePath for f in issue.files if f.filePath!="/dev/null")
        for f in issue.cache_score_new:
        # for f in issue.amalgam[:int(len(issue.amalgam)*0.1)]:
            value = []
            value.append(issue.issue_id)
            value.append(f)
            value.extend(issue.cache_score_new[f])
            if f in ground_truth:
                value.append("bug")
            else:
                value.append("no_bug")
            pairs.append(value)
            # print(value)
    return pairs

def evaluate(test):
    ground_truth = [set(f.filePath for f in issue.files if f.filePath!="/dev/null") for issue in test]
    predict_result = [issue.ablots for issue in test]
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

def calculate(issues):
    bugReport = [x for x in issues if x.issue_type == "Bug"]
    print(len(bugReport), end=";")
    train_size = int(len(bugReport) * 0.8)

    test = bugReport[train_size:]
    train = bugReport[:train_size]

    pairs_train = make_pairs(train)
    pairs_test = make_pairs(test)

    result = MLP(pairs_train, pairs_test)
    reRank(test, pairs_test, result)
    evaluate(test)

path = "C:/Users/Feifei/dataset/tracescore"
files = os.listdir(path)
files = ["derby", "drools", "hornetq", "izpack", "keycloak", "log4j2", "railo", "seam2", "teiid", "weld", "wildfly"]
print(";MAP;MRR;Top 1;Top 5;Top 10;P@1;P@5;P@10;R@1;R@5;R@10;Top 1%; Top 2%;Top 5%;Top 10%;Top 20%;Top 50%;R@1%;R@2%;R@5%;R@10%;R@20%;R@50%")
for file in files[10:]:
    # file = "wildfly.sqlite3"
    print(file, end=" ")
    filePath = path+"\\"+file + ".sqlite3"
    issues = load_issues(filePath) # only read cache score, cache_id score, ground truth
    calculate(issues)
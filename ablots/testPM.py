# use patrick mader's data set and decision tree to see the result
from scipy.io import arff
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.utils import shuffle
from sklweka.dataset import load_arff, to_nominal_labels
import sklweka.jvm as jvm
from imblearn.under_sampling import RandomUnderSampler
from sklweka.classifiers import WekaEstimator

from evaluation.evaluation import evaluation
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# jvm.start(packages=True)
def J48(train, test):

    x_train = [tmp[1:4] for tmp in train]
    y_train = [tmp[-1] for tmp in train]
    x_test = [tmp[1:4] for tmp in test]
    y_test = [tmp[-1] for tmp in test]
    # y_train = to_nominal_labels(y_train)
    # y_test = to_nominal_labels(y_test)
    y_train = [1 if k=='bug' else 0 for k in y_train]
    y_test = [1 if k=='bug' else 0 for k in y_test]
    x_train = [[0 if i is None else i for i in l] for l in x_train]
    x_test = [[0 if i is None else i for i in l] for l in x_test]
    # for index in range(len(x_train)):
    #     x_train[index][1] = 0
    # for index in range(len(x_test)):
    #     x_test[index][1] = 0
    rus = RandomUnderSampler(random_state=1)
    x_train, y_train = rus.fit_resample(x_train, y_train)
    x_train, y_train = shuffle(x_train, y_train)

    # j48 = WekaEstimator(classname="weka.classifiers.trees.J48", options=["-C", "0.5"])

    # j48 = MLPRegressor(hidden_layer_sizes=(5,), random_state=1, solver="adam", activation='logistic')
    # j48 = MLPClassifier(hidden_layer_sizes=(5,), random_state=1, solver="adam", activation='tanh')
    j48 = DecisionTreeClassifier(criterion="gini", min_samples_split=100, max_depth = 16)
    # j48 = RandomForestClassifier(random_state=1)

    j48.fit(x_train, y_train)
    y_pred = j48.predict(x_test)
    prob = j48.predict_proba(x_test)
    feat_importance = j48.tree_.compute_feature_importances(normalize=False)
    # print(feat_importance)
    # # result = [test[i] for i in range(len(test)) if scores[i]=="_bug"]
    if y_pred[0] == '_bug':
        assert prob[0][0] > prob[0][1]
    if y_pred[0] == '_no_bug':
        assert prob[0][0] < prob[0][1]
    prob = [k[1] for k in prob]
    #
    # for p in prob:
    #     print(p)
    # # print()
    # print(j48.coefs_)
    # print(j48.feature_importances_)
    return prob

def train(project):
    train_data = arff.load(open("C:/Users/Feifei/dataset/tracescore/arffs/"+project+"_train.arff", "r"))
    train_data = train_data['data']
    test_data = arff.load(open("C:/Users/Feifei/dataset/tracescore/arffs/"+project+"_test.arff", "r"))
    test_data = test_data['data']

    map_count = {}
    for i in test_data:
        k = i[0]
        if k in map_count:
            map_count[k] = map_count[k] + 1
        else:
            map_count[k] = 1
    total = 0
    for k, v in map_count.items():
        total = total + v
    average = total/len(map_count)
    print(total/len(map_count))

    prob = J48(train_data, test_data)

    ground_truth = {}
    predict = {}
    for index in range(len(test_data)):
        issue_id = test_data[index][0]
        if issue_id in predict:
            if test_data[index][4] == "bug":
                ground_truth[issue_id].append(index)
            predict[issue_id][index] = prob[index]
        else:
            predict[issue_id] = {}
            predict[issue_id][index] = prob[index]
            ground_truth[issue_id] = []
            if test_data[index][4] == "bug":
                ground_truth[issue_id].append(index)

    for k, v in predict.items():
        sorted_f = sorted(v.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        predict[k] = [x[0] for x in sorted_f]

    ground_truth = [ground_truth[issue] for issue in predict]
    predict = [predict[issue] for issue in predict]
    # evaluation(ground_truth, predict)
files = ["derby", "drools", "hornetq", "izpack", "keycloak", "log4j2", "railo", "seam2", "teiid", "weld", "wildfly"]
for f in files[:]:
    print(f, end=";")
    train(f)


# jvm.stop()
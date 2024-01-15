import pandas as pd
from scipy.stats import ks_2samp
import numpy as np
import seaborn as sns
from  scipy import stats
import matplotlib.pyplot as plt

df = pd.read_excel(r'C:\Users\Feifei\Desktop\saner\saner.xlsx', sheet_name='ks-test', header=None, index_col=None)

# map0 = [x for x in df[1][1:12]]
# mrr0 = [x for x in df[2][1:12]]
# top10 = [x for x in df[3][1:12]]
# top50 = [x for x in df[4][1:12]]
# top100 = [x for x in df[5][1:12]]
#
# map1 = [x for x in df[9][1:12]]
# mrr1 = [x for x in df[10][1:12]]
# top11 = [x for x in df[11][1:12]]
# top51 = [x for x in df[12][1:12]]
# top101 = [x for x in df[13][1:12]]
#
# map2 = [x for x in df[1][17:33]]
# mrr2 = [x for x in df[2][17:33]]
# top12 = [x for x in df[3][17:33]]
# top52 = [x for x in df[4][17:33]]
# top102 = [x for x in df[5][17:33]]
#
# map3 = [x for x in df[9][17:33]]
# mrr3 = [x for x in df[10][17:33]]
# top13 = [x for x in df[11][17:33]]
# top53 = [x for x in df[12][17:33]]
# top103 = [x for x in df[13][17:33]]





for k in range(1,6):
    data1 = [x for x in df[k][1:12]]
    data2 = [x for x in df[k][17:33]]
    x = ks_2samp(data1, data2)
    print(x)

    fig = plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    sns.kdeplot(data1)
    sns.kdeplot(data2)
    plt.show()

print()
for k in range(9,14):
    data1 = [x for x in df[k][1:12]]
    data2 = [x for x in df[k][17:33]]
    x = ks_2samp(data1, data2)
    print(x)

    fig = plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    sns.kdeplot(data1)
    sns.kdeplot(data2)
    plt.show()

print()
for k in range(16,21):
    data1 = [x for x in df[k][1:12]]
    data2 = [x for x in df[k][17:33]]
    x = ks_2samp(data1, data2)
    print(x)

    fig = plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    sns.kdeplot(data1)
    sns.kdeplot(data2)
    plt.show()
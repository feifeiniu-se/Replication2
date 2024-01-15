import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

fig, ax = plt.subplots()


df = pd.read_excel(r'C:\Users\Feifei\Desktop\saner\saner.xlsx', sheet_name='ks-test', header=None, index_col=None)

# # TraceScore
# map0 = [x for x in df[1][1:12]]
# mrr0 = [x for x in df[2][1:12]]
# top10 = [x for x in df[3][1:12]]
# top50 = [x for x in df[4][1:12]]
# top100 = [x for x in df[5][1:12]]
#
# map2 = [x for x in df[1][17:33]]
# mrr2 = [x for x in df[2][17:33]]
# top12 = [x for x in df[3][17:33]]
# top52 = [x for x in df[4][17:33]]
# top102 = [x for x in df[5][17:33]]

# # ABLoTS
# map0 = [x for x in df[9][1:12]]
# mrr0 = [x for x in df[10][1:12]]
# top10 = [x for x in df[11][1:12]]
# top50 = [x for x in df[12][1:12]]
# top100 = [x for x in df[13][1:12]]
#
# map2 = [x for x in df[9][17:33]]
# mrr2 = [x for x in df[10][17:33]]
# top12 = [x for x in df[11][17:33]]
# top52 = [x for x in df[12][17:33]]
# top102 = [x for x in df[13][17:33]]

# TraceScore improvement
map0 = [x for x in df[16][1:12]]
mrr0 = [x for x in df[17][1:12]]
top10 = [x for x in df[18][1:12]]
top50 = [x for x in df[19][1:12]]
top100 = [x for x in df[20][1:12]]

map2 = [x for x in df[16][17:33]]
mrr2 = [x for x in df[17][17:33]]
top12 = [x for x in df[18][17:33]]
top52 = [x for x in df[19][17:33]]
top102 = [x for x in df[20][17:33]]


data = [map0, map2, mrr0, mrr2, top10, top12, top50, top52, top100, top102]
# 用positions参数设置各箱线图的位置 
ax.boxplot(data, positions=[0, 1, 3, 4, 6, 7, 9, 10, 12, 13])  # position
ax.set_xticklabels(["original", "extended", "original", "extended", "original", "extended", "original", "extended", "original", "extended"], rotation=30, ha='right')  #x-axis
# ax.set_xticklabels(["MAP", "MRR", "Top 1", "Top 5", "Top 10"])
# plt.title("TraceScore")
plt.ylabel("Score")
plt.savefig(r"C:\Users\Feifei\Desktop\saner\improvement.jpg", dpi=1500)
plt.show()

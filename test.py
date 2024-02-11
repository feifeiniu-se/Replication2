dict_all = {}
dict_cache = {}
dict_bluir = {}
union_candidate = ['d', 'j', 'v', 'p', 's']
for f in union_candidate:
    dict_all[f] = 0
    dict_cache[f] = 0
    dict_bluir[f] = 0
dict_all['j'] += 1
dict_all = list(dict_all.values())
print(dict_all)
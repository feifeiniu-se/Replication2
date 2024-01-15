dictt = {'a': 0, 'b': 7, 'c': 5, 'm': 2}
# ordered_cache_score = sorted(dictt.items(), key=lambda x: x[1], reverse=True)
# cache_candidate = [x[0] for x in ordered_cache_score]
# print(cache_candidate.index('l') if 'l' in cache_candidate else 999)
# cache_candidate = set(cache_candidate)
# seta = {'a', 'b', 'c', 'p', 'x'}
# setb = {'a', 'd', 'c', 'k'}
# setc = {'x', 'c'}
# print(seta.intersection(setb.union(setc)))

# from scipy import spatial
# vec1 = [1, 1, 1, 4, 3, 3, 2, 3, 1, 1]
# vec2 = [0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
# cos_sim = 1 - spatial.distance.cosine(vec1, vec2)
# print(cos_sim)


# seg_set={'a', 'b', 'c', 'd'}
# dict = {}
# for i in seg_set:
#     dict[i] = 0
# dict['b'] += 1
# print(dict)

# dictt['ooo'] = 9
# dictt['b'] += 1
# print(dictt)

test_map = {}
test_map['a'] = 9
test_map['b'] = 77
pp = test_map['a']
pp = 10
print(test_map)

from scipy.stats import pearsonr
import numpy as np

x = np.array([2864,7931, 2216, 1113, 6415, 2399, 2787, 1671, 2332, 5160, 9858, 1024, 3595, 3703, 13192, 1375, 4657, 11720, 4657, 4204, 3423, 5482, 1381, 3866, 1055, 2953, 900, 345, 82, 155, 73, 198, 371, 857, 35, 767, 304, 643, 114])

# # MAP
y1 = np.array([0.312, 0.272, 0.37, 0.37, 0.234, 0.391, 0.286, 0.339, 0.12, 0.252, 0.334, 0.322, 0.335, 0.31, 0.416, 0.388, 0.398, 0.234, 0.357, 0.37, 0.474, 0.321, 0.337, 0.257, 0.406, 0.16, 0.422, 0.124, 0.349, 0.578, 0.674, 0.488, 0.43, 0.393, 0.502, 0.422, 0.481, 0.169, 0.606])
y2 = np.array([0.275, 0.277, 0.372, 0.385, 0.232 , 0.410 , 0.289 , 0.345 , 0.147 , 0.255, 0.333, 0.315, 0.343, 0.311, 0.398, 0.397, 0.354, 0.18, 0.364, 0.382, 0.481, 0.295, 0.343, 0.288, 0.424, 0.159, 0.440 , 0.144, 0.325, 0.565, 0.719, 0.49, 0.453, 0.385, 0.451, 0.446, 0.506, 0.181, 0.611])
y3 = np.array([0.294, 0.283, 0.375, 0.352, 0.243, 0.391, 0.288, 0.345, 0.138, 0.255, 0.34, 0.336, 0.359, 0.301, 0.427, 0.403, 0.412, 0.247, 0.384, 0.378, 0.477, 0.34, 0.357, 0.292, 0.431, 0.159, 0.444, 0.17, 0.359, 0.58, 0.686, 0.489, 0.296, 0.411, 0.497, 0.407, 0.407, 0.199, 0.615])


pc1 = pearsonr(x, y1)
pc2 = pearsonr(x, y2)
pc3 = pearsonr(x, y3)

print("MAP：" + str(pc1[0]) + " " + str(pc1[1]) + " " + str(pc2[0]) + " " + str(pc2[1]) + " " + str(pc3[0]) + " " + str(pc3[1]))

# print("相关系数：", pc2[0], end=" ")
# print("显著性水平：", pc1[1], end=" ")




#
#
# # MRR FW,LR,CombSUM
y1 = np.array([0.478, 0.464, 0.555, 0.493, 0.377, 0.541, 0.398, 0.402, 0.169, 0.445, 0.441, 0.477, 0.462, 0.505, 0.56, 0.458, 0.528, 0.4, 0.483, 0.536, 0.623, 0.466, 0.416, 0.391, 0.496, 0.3, 0.537, 0.25, 0.465, 0.637, 0.762, 0.523, 0.551, 0.687, 0.551, 0.533, 0.667, 0.271, 0.714])
y2 = np.array([0.432, 0.473, 0.559, 0.504, 0.374 , 0.538 , 0.406 , 0.412 , 0.202 , 0.447, 0.439, 0.471, 0.476, 0.506, 0.539, 0.47, 0.474, 0.293, 0.491, 0.550 , 0.642, 0.415, 0.43, 0.438, 0.513, 0.303, 0.564 , 0.275, 0.424, 0.624, 0.823, 0.525, 0.606, 0.674, 0.505, 0.559, 0.667, 0.323, 0.735])
y3 = np.array([0.461, 0.487, 0.561, 0.452, 0.392, 0.504, 0.392, 0.412, 0.19, 0.448, 0.459, 0.51, 0.492, 0.496, 0.587, 0.463, 0.542, 0.422, 0.511, 0.536, 0.641, 0.493, 0.437, 0.436, 0.522, 0.303, 0.577, 0.271, 0.468, 0.639, 0.762, 0.523, 0.447, 0.7, 0.562, 0.501, 0.479, 0.329, 0.735])
pc1 = pearsonr(x, y1)
pc2 = pearsonr(x, y2)
pc3 = pearsonr(x, y3)

print("MRR：" + str(pc1[0]) + " " + str(pc1[1]) + " " + str(pc2[0]) + " " + str(pc2[1]) + " " + str(pc3[0]) + " " + str(pc3[1]))

#
# # Top1
y1 = np.array([0.36, 0.339, 0.426, 0.391, 0.247, 0.416, 0.267, 0.308, 0.1, 0.33, 0.333, 0.347, 0.33, 0.389, 0.456, 0.331, 0.398, 0.29, 0.343, 0.403, 0.516, 0.336, 0.296, 0.275, 0.379, 0.22, 0.383, 0.176, 0.29, 0.548, 0.636, 0.455, 0.409, 0.571, 0.4, 0.41, 0.565, 0.182, 0.625])
y2 = np.array([0.315, 0.342, 0.426, 0.406, 0.247 , 0.404 , 0.283 , 0.321 , 0.127 , 0.339, 0.326, 0.347, 0.347, 0.389, 0.419, 0.336, 0.337, 0.179, 0.363, 0.418, 0.531, 0.295, 0.309, 0.333, 0.394, 0.22, 0.415 , 0.206, 0.226, 0.516, 0.727, 0.455, 0.455, 0.571, 0.333, 0.438, 0.565, 0.273, 0.625])
y3 = np.array([0.351, 0.37, 0.426, 0.344, 0.266, 0.393, 0.267, 0.314, 0.115, 0.339, 0.348, 0.4, 0.361, 0.37, 0.496, 0.323, 0.409, 0.315, 0.382, 0.388, 0.531, 0.377, 0.316, 0.333, 0.394, 0.22, 0.447, 0.176, 0.29, 0.548, 0.636, 0.455, 0.364, 0.607, 0.4, 0.387, 0.391, 0.273, 0.625])

pc1 = pearsonr(x, y1)
pc2 = pearsonr(x, y2)
pc3 = pearsonr(x, y3)
print("Top 1：" + str(pc1[0]) + " " + str(pc1[1]) + " " + str(pc2[0]) + " " + str(pc2[1]) + " " + str(pc3[0]) + " " + str(pc3[1]))

#
# # Top 5
y1 = np.array([0.615, 0.607, 0.704, 0.594, 0.525, 0.719, 0.567, 0.532, 0.208, 0.562, 0.565, 0.587, 0.622, 0.63, 0.67, 0.618, 0.697, 0.551, 0.647, 0.701, 0.742, 0.624, 0.546, 0.536, 0.606, 0.407, 0.745, 0.294, 0.677, 0.742, 0.909, 0.545, 0.818, 0.786, 0.8, 0.668, 0.783, 0.364, 0.875])
y2 = np.array([0.567, 0.630 , 0.722, 0.594, 0.506 , 0.708 , 0.550 , 0.519 , 0.254 , 0.554, 0.565, 0.613, 0.611, 0.63, 0.689, 0.62, 0.635, 0.415, 0.644, 0.716, 0.781, 0.551, 0.533, 0.609, 0.621, 0.418, 0.755 , 0.324, 0.645, 0.774, 0.909, 0.636, 0.818, 0.75, 0.733, 0.705, 0.783, 0.364, 0.875])
y3 = np.array([0.59, 0.638, 0.741, 0.594, 0.551, 0.64, 0.55, 0.538, 0.238, 0.554, 0.587, 0.613, 0.652, 0.648, 0.681, 0.633, 0.702, 0.564, 0.664, 0.731, 0.773, 0.628, 0.566, 0.609, 0.636, 0.418, 0.745, 0.353, 0.677, 0.742, 0.909, 0.455, 0.545, 0.786, 0.8, 0.631, 0.609, 0.364, 0.875])

pc1 = pearsonr(x, y1)
pc2 = pearsonr(x, y2)
pc3 = pearsonr(x, y3)
print("Top 5：" + str(pc1[0]) + " " + str(pc1[1]) + " " + str(pc2[0]) + " " + str(pc2[1]) + " " + str(pc3[0]) + " " + str(pc3[1]))

#
# # Top 10
y1 = np.array([0.725, 0.712, 0.778, 0.672, 0.595, 0.753, 0.65, 0.583, 0.296, 0.634, 0.645, 0.667, 0.741, 0.722, 0.752, 0.726, 0.778, 0.626, 0.746, 0.791, 0.844, 0.71, 0.671, 0.638, 0.712, 0.462, 0.83, 0.353, 0.806, 0.871, 0.909, 0.818, 0.909, 0.964, 0.933, 0.747, 0.87, 0.364, 0.875])
y2 = np.array([0.654, 0.728, 0.796, 0.688, 0.601 , 0.787 , 0.650 , 0.590 , 0.350 , 0.643, 0.659, 0.693, 0.736, 0.741, 0.748, 0.739, 0.746, 0.531, 0.751, 0.791, 0.875, 0.658, 0.691, 0.638, 0.727, 0.473, 0.830 , 0.412, 0.806, 0.871, 0.909, 0.818, 0.909, 1, 0.933, 0.76, 0.87, 0.364, 0.875])
y3 = np.array([0.68, 0.739, 0.815, 0.656, 0.614, 0.719, 0.633, 0.583, 0.319, 0.643, 0.674, 0.707, 0.759, 0.722, 0.767, 0.734, 0.788, 0.656, 0.762, 0.791, 0.875, 0.726, 0.704, 0.638, 0.727, 0.473, 0.83, 0.5, 0.839, 0.839, 0.909, 0.818, 0.636, 0.964, 0.933, 0.7, 0.696, 0.364, 0.875])
# # plt.scatter(x, y)

pc1 = pearsonr(x, y1)
pc2 = pearsonr(x, y2)
pc3 = pearsonr(x, y3)
print("Top 10：" + str(pc1[0]) + " " + str(pc1[1]) + " " + str(pc2[0]) + " " + str(pc2[1]) + " " + str(pc3[0]) + " " + str(pc3[1]))


# pc = pearsonr(x, y)
#
# print("相关系数：", pc[0])
# print("显著性水平：", pc[1])
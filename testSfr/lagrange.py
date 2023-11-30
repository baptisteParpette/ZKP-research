import numpy as np

from scipy.interpolate import lagrange

#L 
# 0,0,1,0,0,0,0,0
# 0,0,1,0,0,0,0,0
# 3,0,0,0,0,0,0,0
# 5,0,0,0,0,0,0,0
#10,0,0,0,0,0,0,0
# 3,0,0,0,0,1,1,1

#R = np.array([
#[0,0,1,0,0,0,0,0],
#[0,0,0,1,0,0,0,0],
#[0,0,0,0,1,0,0,0],
#[0,0,0,1,0,0,0,0],
#[0,0,1,0,0,0,0,0],
#[1,0,0,0,0,0,0,0]

#O =
#[0,0,0,1,0,0,0,0]
#[0,0,0,0,1,0,0,0]
#[0,0,0,0,0,1,0,0]
#[0,0,0,0,0,0,1,0]
#[0,0,0,0,0,0,0,1]
#[0,1,0,0,0,0,0,0]

x = np.array([1, 2, 3, 4, 5, 6])

#L y1 = np.array([0, 0, 3, 5, 10, 3])
#L y2 = np.array([1, 1, 0, 0,  0, 0])
#L y3 = np.array([0, 0, 0, 0,  0, 1])

#R y0 = np.array([0, 0, 0, 0,  0, 1])
#R y2 = np.array([1, 0, 0, 0,  1, 0])
#R y3 = np.array([0, 1, 0, 1,  0, 0])
#R y4 = np.array([0, 0, 1, 0,  0, 0])

y0 = 0
y1 = np.array([0, 0, 0, 0,  0, 1])
y2 = 0
y3 = np.array([1, 0, 0, 0,  0, 0])
y4 = np.array([0, 1, 0, 0,  0, 0])
y5 = np.array([0, 0, 1, 0,  0, 0])
y6 = np.array([0, 0, 0, 1,  0, 0])
y7 = np.array([0, 0, 0, 0,  1, 0])

print(y0)
print(lagrange(x, y1))
print(y2)
print(lagrange(x, y3))
print(lagrange(x, y4))
print(lagrange(x, y5))
print(lagrange(x, y6))
print(lagrange(x, y7))



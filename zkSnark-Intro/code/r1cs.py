import numpy as np
import random

# Define the matrices
O = np.array([
[0,0,0,1,0,0,0,0],
[0,0,0,0,1,0,0,0],
[0,0,0,0,0,1,0,0],
[0,0,0,0,0,0,1,0],
[0,0,0,0,0,0,0,1],
[0,1,0,0,0,0,0,0]
])

L = np.array([
[ 0,0,1,0,0,0,0,0],
[ 0,0,1,0,0,0,0,0],
[ 3,0,0,0,0,0,0,0],
[ 5,0,0,0,0,0,0,0],
[10,0,0,0,0,0,0,0],
[ 3,0,0,0,0,1,1,1]
])

R = np.array([
[0,0,1,0,0,0,0,0],
[0,0,0,1,0,0,0,0],
[0,0,0,0,1,0,0,0],
[0,0,0,1,0,0,0,0],
[0,0,1,0,0,0,0,0],
[1,0,0,0,0,0,0,0]
])

# pick random values for x and y
x = random.randint(1,1000)
#x = 5

# this is our orignal formula
v1 = x * x
v2 = x * v1
v3 = 3 * v2
v4 = 5 * v1
v5 = 10 * x
out = v3 + v4 + v5 + 3

w = np.array([1, out, x, v1, v2, v3, v4, v5])

result = O.dot(w) == np.multiply(L.dot(w),R.dot(w))
assert result.all(), "result contains an inequality"

print("-->", w)
import sys
import numpy as np
from numpy import poly1d
from scipy.interpolate import lagrange

errMax = 0.0000001
witness = [1, 553, 5, 25, 125, 375, 125, 50]
x = np.array([1, 2, 3, 4, 5, 6])

def calculPoly(mat):
    Lt = np.transpose(mat)
    res = []
    for i in range(0, len(Lt)):
        y = Lt[i]
        lArray = lagrange(x, y).coeffs
        if (len(lArray) == 1):
            lArray = np.zeros(len(mat))
    
        res.append(lArray)

    return poly1d(np.matmul(np.transpose(res), witness))

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

O = np.array([
[0,0,0,1,0,0,0,0],
[0,0,0,0,1,0,0,0],
[0,0,0,0,0,1,0,0],
[0,0,0,0,0,0,1,0],
[0,0,0,0,0,0,0,1],
[0,1,0,0,0,0,0,0]
])

Uw = calculPoly(L)
Vw = calculPoly(R)
Ww = calculPoly(O)
print("Uw", Uw)
print("Vw", Vw)
print("Ww", Ww)

for i in range(1, 7):    # 7 points d'interpolation
    erreur = abs(Uw(i)*Vw(i)-Ww(i))
    print(erreur)
    assert (erreur < errMax), "L'égalité n'est pas garantie"





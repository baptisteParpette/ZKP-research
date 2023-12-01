import sys
import numpy as np
from numpy import poly1d
from scipy.interpolate import lagrange

np.set_printoptions(linewidth=np.nan)

def calculPolyLagrange(array):
    (horizontal, vertical) = array.shape

    x = np.arange(1, horizontal+1)

    tL = np.transpose(array)
    res = np.empty((vertical, horizontal))

    for i in range(vertical):
        r = lagrange(x,tL[i])
        res[i] = r

    return(np.transpose(res))


L = np.array([
 [0,0,1,0,0,0,0,0],
 [0,0,1,0,0,0,0,0],
 [3,0,0,0,0,0,0,0],
 [5,0,0,0,0,0,0,0],
[10,0,0,0,0,0,0,0],
 [3,0,0,0,0,1,1,1]
])
U = calculPolyLagrange(L)
#print("U :\n", U)

R = np.array([
[0,0,1,0,0,0,0,0],
[0,0,0,1,0,0,0,0],
[0,0,0,0,1,0,0,0],
[0,0,0,1,0,0,0,0],
[0,0,1,0,0,0,0,0],
[1,0,0,0,0,0,0,0]
])
V = calculPolyLagrange(R)
#print("V :\n", V)


O = np.array([
[0,0,0,1,0,0,0,0],
[0,0,0,0,1,0,0,0],
[0,0,0,0,0,1,0,0],
[0,0,0,0,0,0,1,0],
[0,0,0,0,0,0,0,1],
[0,1,0,0,0,0,0,0]
])
W = calculPolyLagrange(O)
#print("W :\n", W)

witness = [1, 553, 5, 25, 125, 375, 125, 50]

Uw = np.matmul(U, witness)
#print(Uw)
Vw = np.matmul(V, witness)
#print(Vw)
Ww = np.matmul(W, witness)
#print(Ww)

t = poly1d([1, -1])*poly1d([1, -2])*poly1d([1, -3])*poly1d([1, -4])*poly1d([1, -5])*poly1d([1, -6])

fu = poly1d(Uw)
fv = poly1d(Vw)
fw = poly1d(Ww)

(h, reste) = ((fu * fv)-fw)/t

print("h \n", h)
print("reste \n", reste)


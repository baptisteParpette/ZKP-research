import sys
import numpy as np
from numpy import poly1d
witness = [1, 553, 5, 25, 125, 375, 125, 50]

U = np.array(
[
[-0.225,0,0.03333,0,0,0.008333,0.008333,0.008333],
[ 3.708,0, -0.625,0,0,  -0.125,  -0.125,  -0.125],
[-23.12,0,  4.417,0,0,  0.7083,  0.7083,  0.7083],
[ 67.79,0, -14.38,0,0,  -1.875,  -1.875,  -1.875],
[-90.15,0,  20.55,0,0,   2.283,   2.283,   2.283],
[    42,0,     -9,0,0,      -1,      -1,      -1]
])

Uw = np.matmul(U, witness)
#print(poly1d(Uw))
#sys.exit()

V = np.array([
[0.008333,0, -0.05, 0.125,-0.08333,0,0,0],
[  -0.125,0,0.8333,-2.208,     1.5,0,0,0],
[  0.7083,0, -5.25, 14.62,  -10.08,0,0,0],
[  -1.875,0, 15.67,-44.79,      31,0,0,0],
[   2.283,0, -22.2, 62.25,  -42.33,0,0,0],
[      -1,0,    12,   -30,      20,0,0,0]
])


Vw = np.matmul(V, witness)
#print(Vw)
#
W = np.array([
[0,0.008333,0,-0.008333,0.04167,-0.08333,0.08333,-0.04167],
[0,  -0.125,0,   0.1667,-0.7917,     1.5, -1.417,  0.6667],
[0,  0.7083,0,   -1.292,  5.708,  -10.08,  8.917,  -3.958],
[0,  -1.875,0,    4.833, -19.21,      31, -25.58,   10.83],
[0,   2.283,0,     -8.7,  29.25,  -42.33,     33,   -13.5],
[0,      -1,0,        6,    -15,      20,    -15,       6]
])


Ww = np.matmul(W, witness)

print(Ww)
#
fu = poly1d(np.flip(Uw))
fv = poly1d(np.flip(Vw))
fw = poly1d(np.flip(Ww))

print("Convol", np.convolve(fu,fv))

T = np.convolve(fu,fv) - np.concatenate((np.flip(Ww), np.zeros(len(np.convolve(fu,fv)) - len(Ww))))
print(T)
t = poly1d([1, -1])*poly1d([1, -2])*poly1d([1, -3])*poly1d([1, -4])*poly1d([1, -5])*poly1d([1, -6])

print(np.polydiv(T,np.flip(t)))

fu = poly1d(Uw)
print(fu)
fv = poly1d(Vw)
print(fv)
fw = poly1d(Ww)
print(fw)

print("Resultat de division")
print(((fu * fv)-fw)/t)
sys.exit()

a = (fu * fv) - fw
print("->", a)
print("->", a)

print(np.polydiv(a, t))
print(np.polydiv(np.flip(a), np.flip(t)))


print("Test")
print(a)
print(poly1d(np.flip(a)))
print(t)
print(poly1d(np.flip(t)))

print(poly1d(np.flip(a))/poly1d(np.flip(t)))


x = poly1d([-1004024,4428125.2,-8320508.191,8785347.6,-5791667.006,2500408.731,-718713.804,136320.039,-16384.911,1130.431,-34.088])

print("x", x)
print("a", poly1d(np.flip(a)))

#print("x/t ->", x / poly1d(np.flip(t)))
#print("a/t ->", poly1d(np.flip(a)) / poly1d(np.flip(t)))
#print("t ->", t)

#
#
#print("TEST")
#a = poly1d([29.5, -87.5, 61])
#b = poly1d([-1, 4, 0])
#c = poly1d([84.5, -246.5, 171])
#t = poly1d([1, -1])*poly1d([1, -2])*poly1d([1, -3])
#
#print((a * b - c) / t)

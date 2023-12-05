# Prouver que si 
# Uw =  4x^5 + 3x^4 + 5x^3 + 3x^2 + 4x 
# Vw =  6x^5 + x^4 + 6x^3 + 6x^2 + 4x + 3 
# Ww =  6x^5 + 4x^4 + 3x^3 + 5x^2 
# t(x) =  x^6 + 6 
# h_quo(x) =  3x^4 + x^3 + x^2 + 2x

import sys;
from py_ecc.bn128 import G1, G2, multiply, add, curve_order, eq, neg, pairing
import galois

#GF = galois.GF(curve_order)
GF = galois.GF(7)


# p(x) = x^2 -2x -8
# x = 30
#p = galois.Poly([1, -2, -8], field=GF)

# Prouver que u*v = w+ht
u = galois.Poly([4, 3, 5, 3, 4, 0], field=GF)
v = galois.Poly([6, 1, 6, 6, 4, 3], field=GF)
w = galois.Poly([6, 4, 3, 5, 0, 0], field=GF)
t = galois.Poly([1, 0, 0, 0, 0, 0, 6], field=GF)
h = galois.Poly([0, 3, 1, 1, 2, 0], field=GF)

# check initial
h_quo = (u * v - w) // t
h_rem = (u * v - w) % t

#print("Uw", u)
#print("Vw", v)
#print("Ww", w)
#print("t(x)", t)

#print(h)

print(h_quo)
print(h_rem)
if (h_rem != 0):
    print("Les équations sont cassées")
    sys.exit()

print("Les équations sont bonnes")

# evaluate at 8 - Normalement c'est le trusted ici
tau = GF(6)

tau_0 = G1
tau_1 = multiply(G1, int(tau))
tau_2 = multiply(G1, int(tau**2))
tau_3 = multiply(G1, int(tau**3))
tau_4 = multiply(G1, int(tau**4))
tau_5 = multiply(G1, int(tau**5))
tau_6 = multiply(G1, int(tau**6))

tauG2_0 = G2
tauG2_1 = multiply(G2, int(tau))
tauG2_2 = multiply(G2, int(tau**2))
tauG2_3 = multiply(G2, int(tau**3))
tauG2_4 = multiply(G2, int(tau**4))
tauG2_5 = multiply(G2, int(tau**5))
tauG2_6 = multiply(G2, int(tau**6))
tauG2_7 = multiply(G2, int(tau**7))
tauG2_8 = multiply(G2, int(tau**8))
tauG2_9 = multiply(G2, int(tau**9))
tauG2_10 = multiply(G2, int(tau**10))

print("Evaluation en x = ", tau)

#X2 = multiply(multiply(G1, int(tau**2)), 1)
#X1 = multiply(neg(multiply(G1, int(tau))), 2)
#X0 = multiply(neg(G1), 8)

# 4x^5 + 3x^4 + 5x^3 + 3x^2 + 4x 
X5 = multiply(tauG2_5, 4)
X4 = multiply(tauG2_4, 3)
X3 = multiply(tauG2_3, 5)
X2 = multiply(tauG2_2, 3)
X1 = multiply(tauG2_1, 4)
X0 = multiply(tauG2_0, 0)
encodeCoeffU=(add(add(add(add(add(X0, X1), X2),X3),X4),X5))
print("U=",encodeCoeffU)

# 6x^5 + x^4 + 6x^3 + 6x^2 + 4x + 3
X5 = multiply(tau_5, 6)
X4 = multiply(tau_4, 1)
X3 = multiply(tau_3, 6)
X2 = multiply(tau_2, 6)
X1 = multiply(tau_1, 4)
X0 = multiply(tau_0, 3)
encodeCoeffV=(add(add(add(add(add(X0, X1), X2),X3),X4),X5))
print("V",encodeCoeffV)

# 6x^5 + 4x^4 + 3x^3 + 5x^2
X5 = multiply(tauG2_5, 6)
X4 = multiply(tauG2_4, 4)
X3 = multiply(tauG2_3, 3)
X2 = multiply(tauG2_2, 5)
X1 = multiply(tauG2_1, 0)
X0 = multiply(tauG2_0, 0)
encodeCoeffW=(add(add(add(add(add(X0, X1), X2),X3),X4),X5))
print("W",encodeCoeffW)

# h*t 3x^10 + x^9 + x^8 + 2x^7 + 4x^4 + 6x^3 + 6x^2 + 5x
X10 = multiply(tauG2_10, 3)
X9 = multiply(tauG2_9, 1)
X8 = multiply(tauG2_8, 1)
X7 = multiply(tauG2_7, 2)
X6 = multiply(tauG2_6, 0)
X5 = multiply(tauG2_5, 0)
X4 = multiply(tauG2_4, 4)
X3 = multiply(tauG2_3, 6)
X2 = multiply(tauG2_2, 6)
X1 = multiply(tauG2_1, 5)
X0 = multiply(tauG2_0, 0)
encodeCoeffHT=(add(add(add(add(add(add(add(add(add(add(X0, X1), X2),X3),X4),X5),X6),X7),X8),X9),X10))

# 3x^4 + x^3 + x^2 + 2x
#X4 = multiply(tauG2_4, 3)
#X3 = multiply(tauG2_3, 1)
#X2 = multiply(tauG2_2, 1)
#X1 = multiply(tauG2_1, 2)
#X0 = multiply(tauG2_0, 0)
#encodeCoeffh=(add(add(add(X0, X1), X2),X3),X4)


#print(encodeCoeffW)
#print(add(encodeCoeffHT,encodeCoeffW))

#multTH = multiply(encodeCoeffT, int(encodeCoeffh))

#print(multiply(encodeCoeffU,encodeCoeffV))
LPairing = pairing(encodeCoeffU, encodeCoeffV)
RPairing = pairing(add(encodeCoeffHT, encodeCoeffW), G1)

print(LPairing == RPairing)



print(LPairing)
print(RPairing)
#if eq(encodePolyResult, encodeCoeffResult):
#    print("elliptic curve points are equal @", encodeCoeffResult)


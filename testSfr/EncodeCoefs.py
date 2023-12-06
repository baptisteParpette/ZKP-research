import sys;
from py_ecc.bn128 import G1, multiply, add, curve_order, eq, neg
import galois

#GF = galois.GF(curve_order)
GF = galois.GF(101)

# Montrer que si x a une valeur :  E(P(x)) <==> c0E(x/G)+c1E(x/G^2)+)
# L'encodage du polynome à la coordonnée X, et également à la somme des coefficients des valeurs de x encodées

# p(x) = x^2 -2x -8
# x = 30
# 
# Encode(P(30) <==> 1*Encode(30^2) -2*Encode(30) -8*Encode(1)

p = galois.Poly([1, -2, -8], field=GF)

# evaluate at 8
tau = GF(6)
print("Evaluation en x = ", tau)

res = int(p(tau)) # Je ne comprends pas ce int() 
print(res)

# Encode(P(30))
encodePolyResult = multiply(G1, res)
print(encodePolyResult)

# 1*Encode(30^2)-2*Encode(30)-8*Encode(1)
X2 = multiply(multiply(G1, int(tau**2)), 1)
X1 = multiply(neg(multiply(G1, int(tau))), 2)
X0 = multiply(neg(G1), 8)
encodeCoeffResult=(add(add(X0, X1), X2))
print(encodeCoeffResult)

if eq(encodePolyResult, encodeCoeffResult):
    print("elliptic curve points are equal @", encodeCoeffResult)


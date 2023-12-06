import sys;
from py_ecc.bn128 import G1, multiply, add, curve_order, eq, neg
import galois

# Travail du préparateur
#GF = galois.GF(curve_order)
GF = galois.GF(36209)                        # BUG: must be higher order than res

tau = GF(6)                         # variable tau choisie, dans l'ordre de Galois, qui pourra être détruite

X5 = multiply(G1, int(tau**5))      # toutes les puissances de coefficients nécessaires pour tous les calculs
X4 = multiply(G1, int(tau**4))
X3 = multiply(G1, int(tau**3))
X2 = multiply(G1, int(tau**2))
X1 = multiply(G1, int(tau))
X0 = G1


# Travail du prouveur
# 4x^5 + 3x^4 + 5x^3 + 3x^2 + 4x 
u5 = multiply(X5, 4)
u4 = multiply(X4, 3)
u3 = multiply(X3, 5)
u2 = multiply(X2, 3)
u1 = multiply(X1, 4)
u0 = multiply(X0, 0)
encodeCoeffU=(add(add(add(add(add(u0, u1), u2),u3),u4),u5))
print("U=",encodeCoeffU)


# Verification a ne jamais faire
u = galois.Poly([4, 3, 5, 3, 4, 0], field=GF)
res = int(u(tau))
print("res: ", res)
print("Uprouf = ", multiply(G1, res))

print(eq(multiply(G1, res), (add(add(add(add(add(u0, u1), u2),u3),u4),u5))))

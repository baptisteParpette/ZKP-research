from py_ecc.bn128 import G1, multiply, add, neg, eq


# 39 = x^3 -4x^2 + 3^x -1 // Sol : 5

Res = multiply(G1, 39)

X3 = multiply(multiply(G1, 5**3), 1)
X2 = multiply(neg(multiply(G1, 5**2)), 4)
X1 = multiply(multiply(G1, 5), 3)
X0 = multiply(neg(G1), 1)


print(Res == add(add(add(X0, X1), X2), X3))



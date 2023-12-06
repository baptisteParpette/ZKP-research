from py_ecc.bn128 import G1, G2, multiply, add, neg, eq
#4x^5 + 3x^4 + 5x^3 + 3x^2 - 4x = 15055

print("Uw(5) =", multiply(G1, 15055))

X5 = multiply(G1, 5**5)
X4 = multiply(G1, 5**4)
X3 = multiply(G1, 5**3)
X2 = multiply(G1, 5**2)
X1 = multiply(G1, 5)
X0 = G1

c5 = multiply(X5, 4)
c4 = multiply(X4, 3)
c3 = multiply(X3, 5)
c2 = multiply(X2, 3)
c1 = multiply(neg(X1), 4)

print("Somme(coefficient) = ", add(add(add(add(c1,c2),c3),c4),c5))

print(multiply(G1, 15055) == add(add(add(add(c1,c2),c3),c4),c5))

#print("G1", G1)
#print("G1 + G1", add(G1,G1))
#print("2G1", multiply(G1, 2))

#print("G2",G2)
#print("G2 + G2", add(G2, G2))
#print("2G2", multiply(G2, 2))

# 39 = x^3 -4x^2 + 3^x -1 // Sol : 5

#Res = multiply(G1, 39)

#X3 = multiply(multiply(G1, 5**3), 1)
#X2 = multiply(neg(multiply(G1, 5**2)), 4)
#X1 = multiply(multiply(G1, 5), 3)
#X0 = multiply(neg(G1), 1)
#

#print(Res == add(add(add(X0, X1), X2), X3))



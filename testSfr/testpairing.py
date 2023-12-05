from py_ecc.bn128 import neg, multiply, G1, G2, pairing, curve_order


print(neg(multiply(G1, 4)))


A = multiply(G2, 5)
B = multiply(G1, 6)

C = multiply(G2, 5*6)

print(pairing(A, B) == pairing(C, G1))

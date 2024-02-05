import sys
from py_ecc.bn128 import neg, multiply, G1, G2, G12, pairing, curve_order, add, FQ12
#from c.bn128.bn128_field_elements import FQ12

A = multiply(G1, 5)
B = multiply(G2, 6)
C = multiply(G1, 5*6)


alpha = 12
beta = 16

left = add(multiply(G1,alpha), A)
right = add(multiply(G2, beta), B)

alphaBeta = pairing(multiply(G2, beta), multiply(G1, alpha))
APaired = pairing(G2, multiply(A, beta))
BPaired = pairing(G2, multiply(multiply(G1, 6), alpha))

rightPairing = alphaBeta*APaired*BPaired*pairing(G2, C)


print(pairing(right, left) == rightPairing)
sys.exit()


print(pairing(B, A) == pairing(G2, C)) # un bug de librairie python oblige de faire G2 -> G1
sys.exit()

#neutral_element = bn128.FQ12([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

A = multiply(G12, 2)
print(A)
sys.exit()
#B = multiply(G12, 3)
#C = multiply(G12, 5)

#print(add(A, B) == C)


#print(neg(multiply(G1, 4)))


A = multiply(G1, 1)
B = multiply(G2, 2)
C = pairing(B, A)

#C2 = pairing(B, neg(A))

#print(C + C2)
#print(C * C2)
#print(FQ12.one())

D = multiply(G2, 1)
E = multiply(G1, 2)
F = pairing(D, E)

print(F + C)
print(F + C + FQ12.one())
print(F + C + FQ12.zero())

#print(FQ12.zero())


#A = multiply(G2, 1)
#B = multiply(G1, 2)
#C = pairing(A, B)
#print("\n\n\n", C)


#D = (FQ12(C.coeffs))
#print(D)

#print(add(D, G12))

#print("--->", FQ12(C.coeffs))
#print("--->", multiply(G12, 2))


#A2 = multiply(G1, 10)
#B2 = multiply(G2, 12)
#C2 = pairing(B2, A2)


#E = add(C2, C)


#C = multiply(G2, 5*6)

#print(pairing(A, B) == pairing(C, G1))

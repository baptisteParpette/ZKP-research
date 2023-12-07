from py_ecc.bn128 import neg, multiply, G1, G2, pairing, curve_order, add
import sys


#print(neg(multiply(G1, 4)))


A = multiply(G2, 5)
B = multiply(G1, 6)

C = multiply(G2, 5*6)

#print(pairing(A, B) == pairing(C, G1))


A2 = multiply(A, 2)
B2 = multiply(B, 3)


P_2G2 = multiply(G2, 2)
P_3G1 = multiply(G1, 3)

P12 = pairing(multiply(G2, 2), multiply(G1, 3))
C12 = pairing(C, G1)

#print("C ->", C12)
#print("P12 ->", P12)

def add12(p1, p2):
    #print(p1)
    if p1 is None or p2 is None:
        return p1 if p2 is None else p2
    print(p1(0))
    x1, y1, z1, a1, b1, c1, d1, e1, f1, g1, h1, i1 = iter(p1)
    x2, y2 = p2

    if x2 == x1 and y2 == y1:
        return double(p1)
    elif x2 == x1:
        return None
    else:
        l = (y2 - y1) / (x2 - x1)
    newx = l**2 - x1 - x2
    newy = -l * newx + l * x1 - y1
    assert newy == (-l * newx + l * x2 - y2)
    return (newx, newy)


D = add12(P12, C)

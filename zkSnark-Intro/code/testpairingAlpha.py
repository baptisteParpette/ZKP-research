from py_ecc.bn128 import neg, multiply, G1, G2, pairing, curve_order, add
import sys


AG1 = multiply(G1, 1)
BG2 = multiply(G2, 2)

CG1 = multiply(G1, 2)

#print(pairing(BG2, AG1) == pairing(G2, CG1))

#
alphaG1 = multiply(G1, 2)
betaG2 = multiply(G2, 3)

Aprime = add(AG1, alphaG1)
Bprime = add(BG2, betaG2)

somme = pairing(betaG2, alphaG1)

#Cpairing = pairing(Bprime, Aprime)
#pairingC = pairing(G2, CG1)

print("-->", pairing(Bprime, Aprime))

print("--->", (int)((somme * pairing(G2, CG1)).coeffs[0])%curve_order)

#print("-->", Cpairing + somme)
#print("-->", pairingC + somme)



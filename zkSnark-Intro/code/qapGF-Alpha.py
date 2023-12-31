import sys
import numpy as np
import galois
from py_ecc.bn128 import curve_order, multiply, G1, G2, add, neg, pairing

def calculC(witness, privG1, h, txiG1, s, alphaG1, r, betaG1, deltaG1):
  
    htTG1 = None
    for i in range(0, len(h)):
        htTG1 = add(htTG1, multiply(txiG1[len(h)-i-1], (int)(h.coeffs[i])))

    privWG1 = None
    for i in range(0, len(privG1)):
        tmp = multiply(privG1[i], (int)(witness[i+nbPublicVars]))
        privWG1 = add(privWG1, tmp)

    sA1 = multiply(alphaG1, (int)(s))
    rB1 = multiply(betaG1, (int)(r))

    rsDeltaG1 = multiply(deltaG1, (int)(r*s))

    return add(add(add(add(rB1, neg(rsDeltaG1)), sA1), htTG1), privWG1)


def calculAB(alphaG1, witness, u, powerTauG1, r, deltaG1):
    transpose = np.transpose(u)
    (nbVariables, nbPortes) = transpose.shape

    sommeUwiTG1 = None
    for i in range(0, nbVariables):
        UiTG1 = None
        for j in range(0, nbPortes):
            #print(j, i, u[j, i], "T", nbPortes-j-1)
            #print(u[j, i], "->", powerTauG1[nbPortes-j-1])
            UiTG1 = add(UiTG1, multiply(powerTauG1[nbPortes-j-1], (int)(u[j, i])))
            
        sommeUwiTG1 = add(sommeUwiTG1, multiply(UiTG1, (int)(witness[i])))
 
    return add(add(alphaG1, sommeUwiTG1), multiply(deltaG1, (int)(r)))

def multCoeffs(decalage, matrice, tau): # alpha*u(tau)|beta*v[tau)|w[tau]
    mtranspose = np.transpose(matrice)
    (nbVariables, nbPortes) = mtranspose.shape
    res = []
    for i in range(0, nbVariables):
       coeff = galois.Poly(mtranspose[i], field=GF)
       #print(coeff)
       res.append(decalage*coeff(tau))
    return res

def calculParams(betas, alphas, ws, gamma, delta):
    #print(betas)
    #print(nbPublicVars)
    public = []
    for i in range(0, nbPublicVars):
        #print(i)
        public.append((betas[i]+alphas[i]+ws[i])/gamma)
    
    private = []
    for i in range(nbPublicVars, len(betas)):
        #print(i)
        private.append((betas[i]+alphas[i]+ws[i])/delta)

    return(public, private)

def trustedSetup(U, V, W):
    (nbPortes, nbVariables) = U.shape # U, V et W ont la même forme  3x^(nbPortes)+3x^(nbPortes-1)...

    tau = GF(75)  # Variable aléatoire. x dans papier groth16

    alpha = GF(2)
    beta  = GF(3)
    gamma = GF(5)
    delta = GF(11)

    puissancesXi = []
    for i in range(0, nbPortes):
      puissancesXi.append((int)(tau**i))

    #print(puissancesXi[3])
    #print((int)(tau**3))

    tXi = []
    t = generateT(nbPortes, GF) # x^6 + 80x^5 + 74x^4 + 73x^3 + 8x^2 + 54x + 13 (x-1)(x-2)...(x-n)
    for i in range(0, nbPortes-1):
      tXi.append(puissancesXi[i]*t(tau)/delta)

    #print(U)
    betaUiX = multCoeffs(beta, U, tau)
    alphaViX = multCoeffs(alpha, V, tau)
    WiW = multCoeffs(1, W, tau)

    (pub, priv) = calculParams(betaUiX, alphaViX, WiW, gamma, delta)

    return ((
       multiply(G1, int(alpha)),
       multiply(G1, int(beta)),
       multiply(G1, int(delta)), 
      [multiply(G1,int(elem)) for elem in puissancesXi],
      [multiply(G1,int(elem)) for elem in tXi],
      [multiply(G1,int(elem)) for elem in pub],
      [multiply(G1,int(elem)) for elem in priv],
      ), (
       multiply(G2, int(beta)),
       multiply(G2, int(gamma)),
       multiply(G2, int(delta)), 
      [multiply(G2,int(elem)) for elem in puissancesXi]
      )
    )

def calculPolyLagrangeGF(array):
    (horizontal, vertical) = array.shape

    x = GF(np.arange(1, horizontal+1)) # x = [1, 2, 3, 4]

    tL = np.transpose(array)
    res = GF(np.zeros((vertical, horizontal), dtype=int))

    for i in range(vertical):
        r = galois.lagrange_poly(x,tL[i])
        res[i] = r.coefficients()

    return(np.transpose(res))

def generateT(size, ordre):
    '''
    (6) = (x-1)(x-2)(x-3)(x-4)(x-5)(x-6)
    '''
    result_poly = galois.Poly([1], field=ordre)  # Start with the polynomial '1' in the given field
    for val in range(1, size+1):
        # Multiply the result by (x - val) for each val in values
        result_poly *= galois.Poly([1, -val], field=ordre)
    return result_poly 

p = curve_order
#p = 101
GF = galois.GF(p) 
nbPublicVars = 2 # [1, out, x, u1, u2...] l = 1 car 1 et out sont publiques

np.set_printoptions(linewidth=np.nan)

#On part des matrices initiales. Indépendantes du corps de calcul
L = GF(np.array([
 [0,0,1,0,0,0,0,0],
 [0,0,1,0,0,0,0,0],
 [3,0,0,0,0,0,0,0],
 [5,0,0,0,0,0,0,0],
[10,0,0,0,0,0,0,0],
 [3,0,0,0,0,1,1,1]
]) % p)

R = GF(np.array([
[0,0,1,0,0,0,0,0],
[0,0,0,1,0,0,0,0],
[0,0,0,0,1,0,0,0],
[0,0,0,1,0,0,0,0],
[0,0,1,0,0,0,0,0],
[1,0,0,0,0,0,0,0]
]) % p)

O = GF(np.array([
[0,0,0,1,0,0,0,0],
[0,0,0,0,1,0,0,0],
[0,0,0,0,0,1,0,0],
[0,0,0,0,0,0,1,0],
[0,0,0,0,0,0,0,1],
[0,1,0,0,0,0,0,0]
]) % p)

witness = [1, 553, 5, 25, 125, 375, 125, 50]
witness = np.array(witness) % p
witness = GF(witness)


#witness = [GF(1%p), GF(553%p), GF(5%p), GF(25%p), GF(125%p), GF(375%p), GF(125%p), GF(50%p)]
U = calculPolyLagrangeGF(L)
V = calculPolyLagrangeGF(R)
W = calculPolyLagrangeGF(O)

#(alphaG1, betaG1, deltaG1, powerTauG1, txiG1, pubG1, privG1)
#(gamma1G1, gamma2G2) = trustedSetup(U,V,W)
#print(gamma1G1)
#print(gamma2G2)
((alphaG1, betaG1, deltaG1, powerTauG1, txiG1, pubG1, privG1), (betaG2, gammaG2, deltaG2, powerTauG2)) = trustedSetup(U,V,W)

r = GF(13)
AprimeG1 = calculAB(alphaG1, witness, U, powerTauG1, r, deltaG1) 
print("AprimeG1", AprimeG1)

s = GF(17)
BprimeG2 = calculAB(betaG2, witness, V, powerTauG2, s, deltaG2)
BprimeG1 = calculAB(betaG1, witness, V, powerTauG1, s, deltaG1)
print("BprimeG1", BprimeG1)
print("BprimeG2", BprimeG2)

#witness = np.array(witness) % p
#witness = GF(witness)
Uw = galois.Poly(np.matmul(U, witness), field=GF)
Vw = galois.Poly(np.matmul(V, witness), field=GF)
Ww = galois.Poly(np.matmul(W, witness), field=GF)

t = generateT(len(L), GF)
print(t)

h_quo = (Uw * Vw - Ww) // t
h_rem = (Uw * Vw - Ww) % t

CprimeG1 = calculC(witness, privG1, h_quo, txiG1, s, AprimeG1, r, BprimeG1, deltaG1)
print("CprimeG1", CprimeG1)

left = pairing(BprimeG2, AprimeG1)
print(left)

sommePub = None
for i in range(0, nbPublicVars):
    sommePub = add(sommePub, multiply(pubG1[i], (int)(witness[i])))

right = pairing(betaG2, alphaG1) * pairing(gammaG2, sommePub) * pairing(deltaG2, CprimeG1)
print(right)

print(right == left)

#print("Uw = ", Uw, "\n")
#print("Vw = ", Vw, "\n")
#print("Ww = ", Ww, "\n")
#print("t(x) = ", t,"\n")
#print("\nh_quo(x) = ", h_quo)
#print("h_rem(x) = ", h_rem)
#if(h_rem == 0):
#    print("=> La preuve est valide")
#else:
#    print("=> La preuve invalide")



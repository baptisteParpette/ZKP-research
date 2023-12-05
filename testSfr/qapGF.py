import sys
import numpy as np
import galois

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

p=7
GF = galois.GF(p) 

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

U_polys = calculPolyLagrangeGF(L);
V_polys = calculPolyLagrangeGF(R);
W_polys = calculPolyLagrangeGF(O);

Uw = galois.Poly(np.matmul(U_polys, witness))
Vw = galois.Poly(np.matmul(V_polys, witness))
Ww = galois.Poly(np.matmul(W_polys, witness))

t = generateT(len(L), GF)

h_quo = (Uw * Vw - Ww) // t
h_rem = (Uw * Vw - Ww) % t

print("Uw = ", Uw, "\n")
print("Vw = ", Vw, "\n")
print("Ww = ", Ww, "\n")
print("t(x) = ", t,"\n")
print("\nh_quo(x) = ", h_quo)
print("h_rem(x) = ", h_rem)
if(h_rem == 0):
    print("=> La preuve est valide")
else:
    print("=> La preuve invalide")



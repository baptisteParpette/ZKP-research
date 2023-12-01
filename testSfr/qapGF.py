import sys
import numpy as np
from numpy import poly1d
from scipy.interpolate import lagrange
import galois
from functools import reduce

#On definit le corps de Galois
GF = galois.GF(1279) 

#np.set_printoptions(threshold=1000)
np.set_printoptions(linewidth=np.nan)

def polynomial_product_in_GF(values, ordre):
    '''
    Fonction qui transforme une liste de valeurs en un polynome dans le corps de Galois GF
    ex: [1,2,3] = (x-1)(x-2)(x-3)
    Il return ce polynome dans le corps de Galois 'ordre'
    
    '''
    result_poly = galois.Poly([1], field=ordre)  # Start with the polynomial '1' in the given field
    for val in values:
        # Multiply the result by (x - val) for each val in values
        result_poly *= galois.Poly([1, -val], field=ordre)
    return result_poly


def interpolate_column(col):
    xs = GF(np.array([i for i in range(1, num_eq+1)]))
    return galois.lagrange_poly(xs, col)

def inner_product_polynomials_with_witness(polys, witness):
    mul_ = lambda x, y: x * y
    sum_ = lambda x, y: x + y
    return reduce(sum_, map(mul_, polys, witness))

#============================================== INPUT =======================================================

#Ce sont les même matrices qu'avant lorsqu'on travaillait avec des entiers
L = np.array([
 [0,0,1,0,0,0,0,0],
 [0,0,1,0,0,0,0,0],
 [3,0,0,0,0,0,0,0],
 [5,0,0,0,0,0,0,0],
[10,0,0,0,0,0,0,0],
 [3,0,0,0,0,1,1,1]
])

R = np.array([
[0,0,1,0,0,0,0,0],
[0,0,0,1,0,0,0,0],
[0,0,0,0,1,0,0,0],
[0,0,0,1,0,0,0,0],
[0,0,1,0,0,0,0,0],
[1,0,0,0,0,0,0,0]
])

O = np.array([
[0,0,0,1,0,0,0,0],
[0,0,0,0,1,0,0,0],
[0,0,0,0,0,1,0,0],
[0,0,0,0,0,0,1,0],
[0,0,0,0,0,0,0,1],
[0,1,0,0,0,0,0,0]
])

witness = [1, 553, 5, 25, 125, 375, 125, 50]

#============================================== CORE CODE =======================================================
num_var=len(witness)
num_eq=len(L)

#On convertit les matrices en matrices de Galois
L_galois = GF(L)
R_galois = GF(R)
O_galois = GF(O)

print("=======================DEBUT=========================\n")
# axis 0 is the columns. apply_along_axis is the same as doing a for loop over the columns and collecting the results in an array
U_polys = np.apply_along_axis(interpolate_column, 0, L_galois)
print("L_galois :\n", L_galois)
print("\nU_polys :")
for elem in U_polys:
    print(" ",elem)

V_polys = np.apply_along_axis(interpolate_column, 0, R_galois)
print("\n\nR_galois :\n", R_galois)
print("\nV_polys :")
for elem in V_polys:
    print(" ",elem)

W_polys = np.apply_along_axis(interpolate_column, 0, O_galois)
print("\n\nO_galois :\n", O_galois)
print("\nW_polys :")
for elem in W_polys:
    print(" ",elem)
print("\n=====================================================")

#Conversion du witness dans le corps de Galois
witness = GF(witness)

fu = inner_product_polynomials_with_witness(U_polys, witness)
print("\nfu :\n", fu)
fv = inner_product_polynomials_with_witness(V_polys, witness)
print("\n\nfv :\n", fv)
fw = inner_product_polynomials_with_witness(W_polys, witness)
print("\n\nfw :\n", fw)

print("\n=====================================================")

values = [i for i in range(1, num_eq+1)] # Car on a 6 colonnes

t = polynomial_product_in_GF(values, GF)

h_quo = (fu * fv - fw) // t
h_rem = (fu * fv - fw) % t

print("\nh_quo(x) = ", h_quo,"\n")
print("\nh_rem(x) = ", h_rem,"\n")
print("t(x) = ", t,"\n")
print("======================FIN============================")


assert fu * fv == fw + h_quo * t, "division has a remainder"


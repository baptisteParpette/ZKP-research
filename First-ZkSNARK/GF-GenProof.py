import zktool as zk
import numpy as np
import sys
from scipy.interpolate import lagrange
import galois
from functools import reduce
import sys;
from py_ecc.bn128 import G1, G2, multiply, add, curve_order, eq, neg, pairing, Z1, Z2
import galois

def transformer_equation(enonce):
    lignes = enonce.split('\n')
    lignes_nettoyees = [ligne.strip() for ligne in lignes if ligne.strip()]
    return lignes_nettoyees

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

p = 21888242871839275222246405745257275088548364400416034343698204186575808495617
GF = galois.GF(p)

eq_input=input("Entrer un polynome (x^3 + x + 5) : ") #METTRE DES COEFFICIENTS >=0, aucune negatif pour l'instant

#Les équations va etre automatique determiné avec votre input (Polynome)
equations = zk.decompose_polynomial(eq_input)

#Voici une méthode rentrer les équations manuellements:

# Pour tester à la main il faut juste copier coller ses équations dans la variable manual_equation en dessus. Sinon laisser vide (manual_equation="").
# manual_equation='''
# v1 = x * x
# v2 = x * v1
# v3 = 3 * v2
# v4 = 5 * v1
# v5 = 10 * x
# out = v3 + v4 + v5 + 3
# '''
# manual_equation=""

# if manual_equation:
#     equations=transformer_equation(manual_equation)

unique_words = zk.get_unique_words(equations)

print("Modelisation des circuits arithmetiques :")
for eq in equations:
    print(eq)


#création des 3 matrice vides A B C
L= []
R= []
O= []

ref_array=list(unique_words)
print("Vecteur solution :")
print(ref_array)
print(' ')

print("Matrice L R O :\n")
for eq in equations:
    eq_split=eq.split()

    if eq_split[3]=='*':
        vecta=zk.get_position_vector(ref_array, eq_split[2])
        L.append(vecta)
        vectb=zk.get_position_vector(ref_array, eq_split[4])
        R.append(vectb)
        vectc=zk.get_position_vector(ref_array, eq_split[0])
        O.append(vectc)

    if eq_split[3]=='+':
        if "out" in eq:
            list_var = eq_split[2:]
        else:
            list_var = [eq_split[2],eq_split[4]]
        vecta=zk.get_position_vector(ref_array, list_var)
        L.append(vecta)
        vectb=zk.get_position_vector(ref_array, "1")
        R.append(vectb)
        vectc=zk.get_position_vector(ref_array, eq_split[0])
        O.append(vectc)

print("L=")
for ligne in L:
    print(ligne)
print(" ")

print("R=")
for ligne in R:
    print(ligne)
print(" ")

print("O=")
for ligne in O:
    print(ligne)
print(" ")


num_eq = len(L)

#Ici on cherche les coefficients des polynomes de chaque matrice

L=np.array(L)
R=np.array(R)
O=np.array(O)


# On convertit les matrices pour etre convertisable en GF (Chaque valeur est ramenée entre [0, p-1] )
L = L % p
R = R % p
O = O % p
#On convertit les matrices en matrices de Galois
L_galois = GF(L)
R_galois = GF(R)
O_galois = GF(O)

# axis 0 is the columns. apply_along_axis is the same as doing a for loop over the columns and collecting the results in an array
U_polys = np.apply_along_axis(interpolate_column, 0, L_galois)
print("L_galois :\n", L_galois)
print("\nU_polys :")
print(U_polys[0])
# print(" ")
# for elem in U_polys:
#     print(" ",elem)

V_polys = np.apply_along_axis(interpolate_column, 0, R_galois)
print("\n\nR_galois :\n", R_galois)
# print("\nV_polys :")
# for elem in V_polys:
#     print(" ",elem)

W_polys = np.apply_along_axis(interpolate_column, 0, O_galois)
print("\n\nO_galois :\n", O_galois)
# print("\nW_polys :")

# for elem in W_polys:
#     print(" ",elem)




# print(V_polys)
# print(W_polys)
values = {"x": 5}

witness = zk.compute_solution_vector(ref_array, equations, values)
print("\nSolution Vector:", witness)
# print("Vecteur avec variable ",ref_array)

#idem pour le vecteur witness
witness = np.array(witness) % p

num_var=len(witness)
#Conversion du witness dans le corps de Galois
witness = GF(witness)

fu = inner_product_polynomials_with_witness(U_polys, witness)
print("\nfu(x) = ", fu)
fv = inner_product_polynomials_with_witness(V_polys, witness)
print("fv(x) = ", fv)
fw = inner_product_polynomials_with_witness(W_polys, witness)
print("fw(x) = ", fw)
values = [i for i in range(1, num_eq+1)] # Car on a 6 colonnes

t = polynomial_product_in_GF(values, GF)

h_quo = (fu * fv - fw) // t
h_rem = (fu * fv - fw) % t

print("\nh_quo(x) = ", h_quo)
print("h_rem(x) = ", h_rem)
print("t(x) = ", t,"\n")
if(h_rem == 0):
    print("=> La preuve est valide")
else:
    print("=> La preuve invalide")


u=fu
v=fv
w=fw
t=t

# check initial
h_quo = (u * v - w) // t
h_rem = (u * v - w) % t
print("\n======== Affichage de nos polynomes ========")

print("u = ", u)
print("v = ", v)
print("w = ", w)
print("t = ", t)
#print("h = ", h)
print("  -> h_quo = ", h_quo)
print("  -> h_rem = ", h_rem)

if (h_rem != 0):
    print("\n!! Les équations sont cassées !! ")
    sys.exit()
print("\n => Les équations sont bonnes")
h=h_quo

nombre_var=len(u)
tau = GF(3)
print("tau =  ", tau)

tau_G1=[]
for i in range(0, nombre_var):
    tau_G1.append(multiply(G1, int(tau**i)))
tau_G2=[]
for i in range(0, nombre_var):
    tau_G2.append(multiply(G2, int(tau**i)))

tau_t_G1=[]
t_tau=int(t(tau))
print("t(tau)=",t_tau)
for i in range(0, nombre_var):
    tau_t_G1.append(multiply(multiply(G1, t_tau),int(tau**i)))

print("\n======== Calcul de tau^i*G1 , tau^i*G2 et tau^i_t_G1========")
print("[tau_G1]1 = ", tau_G1)
print("[tau_G2]2 = ", tau_G2)
print("[tau_t_G1]1 = ", tau_t_G1)


print("\n======== Calcul de [A],[B] et [C] ========")
# CALCULE DE encodeCoeffU noté A
A=0
encodeCoeffU=Z1
for i in range(0, nombre_var):
    coeff_enc=multiply(tau_G2[i], int(u.coeffs[::-1][i]))
    encodeCoeffU=add(encodeCoeffU, coeff_enc)
A=encodeCoeffU    
print("[A]2= ",A)

# CALCULE DE encodeCoeffV noté B
B=0
encodeCoeffV=Z1
for i in range(0, nombre_var):
    coeff_enc=multiply(tau_G1[i], int(v.coeffs[::-1][i]))
    encodeCoeffV=add(encodeCoeffV, coeff_enc)
B=encodeCoeffV
print("[B]1= ",B)

# CALCULE DE encodeCoeffW
encodeCoeffW=Z2
for i in range(0, nombre_var):
    coeff_enc=multiply(tau_G1[i], int(w.coeffs[::-1][i]))
    encodeCoeffW=add(encodeCoeffW, coeff_enc)
print("[W]1=",encodeCoeffW)

# CALCULE DE encodeCoeffHT
encodeCoeffHT=Z1
for i in range(0, len(h.coeffs)):
    coeff_enc=multiply(tau_t_G1[i], int(h.coeffs[::-1][i]))
    encodeCoeffHT=add(encodeCoeffHT, coeff_enc)
print("[HT]1=",encodeCoeffHT)

# CALCULE DE encodeCoeffU + encodeCoeffV
C=add(encodeCoeffHT,encodeCoeffW)
print("[C]1=",C)

#Test de pairing
LPairing = pairing(A, B)
RPairing = pairing(G2, C)

print("\nTest du pairing p(A,B)==p(G2,C) vaut : ",LPairing == RPairing)
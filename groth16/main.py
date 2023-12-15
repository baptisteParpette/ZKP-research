import sys
import zktool as zk
import numpy as np
import galois
from functools import reduce
import py_ecc.bn128
from py_ecc.bn128 import G1, G2, multiply, add, curve_order, eq, neg, pairing, Z1, Z2
import galois
from functools import reduce
import numpy as np
from operator import add
import pickle
import os

# 1. On demande à l'utilisateur de rentrer une équation
eq_input=input("Enter an equation (ex: x^3+x+5) : ") #METTRE DES COEFFICIENTS >=0, aucune negatif pour l'instant

#On definit le corps de Galois
p=21888242871839275222246405745257275088548364400416034343698204186575808495617
#p=101

GF=galois.GF(p)
    
#print("=================== GROTH16 IMPLEMENTATION ===================")
#print("Equation: ",eq_input,"\n")

def transformer_equation(enonce):
    lignes = enonce.split('\n')
    lignes_nettoyees = [ligne.strip() for ligne in lignes if ligne.strip()]
    return lignes_nettoyees

#Les équations va etre automatique determiné avec votre input (Polynome)
#equations = zk.decompose_polynomial(eq_input)

# #Voici une méthode rentrer les équations manuellements:

# # Pour tester à la main il faut juste copier coller ses équations dans la variable manual_equation en dessus. Sinon laisser vide (manual_equation="").
manual_equation='''
v1 = x * x
v2 = x * v1
v3 = 3 * v2
v4 = 5 * v1
v5 = 10 * x
out = v3 + v4 + v5 + 3
'''
# manual_equation=""

if manual_equation:
    equations=transformer_equation(manual_equation)

unique_words = zk.get_unique_words(equations)


print("Modelisation des circuits arithmetiques :")
for eq in equations:
    print(eq)

print("\nEnsemble des varibles =",unique_words)

#création des 3 matrice vides A B C
L= []
R= []
O= []

print("Equations :")
for eq in equations:
    print(eq)
print(" ")

ref_array=list(unique_words)
print("Vecteur solution :")
print(ref_array)
print(' ')

print("Matrice L R O :")
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

def interpolate_column(col):
    xs = GF(np.array([i for i in range(1, num_eq+1)]))
    return galois.lagrange_poly(xs, col)

def inner_product_polynomials_with_witness(polys, witness):
    mul_ = lambda x, y: x * y
    sum_ = lambda x, y: x + y
    return reduce(sum_, map(mul_, polys, witness))

# axis 0 is the columns. apply_along_axis is the same as doing a for loop over the columns and collecting the results in an array
U_polys = np.apply_along_axis(interpolate_column, 0, L_galois)
V_polys = np.apply_along_axis(interpolate_column, 0, R_galois)
W_polys = np.apply_along_axis(interpolate_column, 0, O_galois)

temp_U=[]
for elem in U_polys:
    temp1=[]
    for el in elem.coeffs:
        temp1.append(int(el))
    temp_U.append(temp1)
taille_maximale_U = max(len(sous_tableau) for sous_tableau in temp_U)
U = [sous_tableau + [0] * (taille_maximale_U - len(sous_tableau)) for sous_tableau in temp_U]

temp_V=[]
for elem in V_polys:
    temp1=[]
    for el in elem.coeffs:
        temp1.append(int(el))
    temp_V.append(temp1)
taille_maximale_V = max(len(sous_tableau) for sous_tableau in temp_V)
V = [sous_tableau + [0] * (taille_maximale_V - len(sous_tableau)) for sous_tableau in temp_V]

temp_W=[]
for elem in W_polys:
    temp1=[]
    for el in elem.coeffs:
        temp1.append(int(el))
    temp_W.append(temp1)
taille_maximale_W = max(len(sous_tableau) for sous_tableau in temp_W)
W = [sous_tableau + [0] * (taille_maximale_W - len(sous_tableau)) for sous_tableau in temp_W]

print("Matrice U :")
for ligne in U:
    print(ligne)

print("\nMatrice V :")
for ligne in V:
    print(ligne)

print("\nMatrice W :")
for ligne in W:
    print(ligne)
values = {"x": 5}

witness = zk.compute_solution_vector(ref_array, equations, values)
print("\nSolution Vector:", witness)
print("Vecteur avec variable ",ref_array)

#idem pour le vecteur witness
witness = np.array(witness) % p

num_var=len(witness)
def evaluate_polynomial_galois(coefs, x, GF):
    result = GF(0)
    for coef in coefs:
        result = result * x + GF(coef)
    return int(result)

def evaluate_poly(poly, trusted_points, verbose=False):
    coeff = poly.coefficients()[::-1]
    terms = [multiply(point, int(coeff))
             for point, coeff in zip(trusted_points, coeff)]
    evaluation = terms[0]
    for i in range(1, len(terms)):
        evaluation = add(evaluation, terms[i])

    return evaluation
## TRUSTED SETUP
def trusted_setup(U,V,W,l):
 
    m=len(U)-1
    n=len(U[0])

    #=================================Pour trouver t(x)  ==========================
    values = [i for i in range(1, len(U[0])+1)]
    poly_t = galois.Poly([1], field=GF)
    for val in values:
        poly_t *= galois.Poly([1, -val], field=GF)
    t=[]
    for elem in poly_t.coeffs:
        t.append(int(elem))
    # print("Polynome t= ",t, " donc t(x) = ",poly_t)
    #==============================================================================
    
    x=GF(75)
    print("x = ",int(x))

    t_x=evaluate_polynomial_galois(t, x, GF)
    # print("t(x) = ",t_x)

    alpha = GF(2)
    beta  = GF(3)
    gamma = GF(5)
    delta = GF(11)

    print("alpha = ",int(alpha))
    print("beta = ",int(beta))
    print("gamma = ",int(gamma))
    print("delta = ",int(delta))

    x_power_i=[]
    for i in range(0, n):
        x_power_i.append(x**i)

    U_polys=[]
    V_polys=[]
    W_polys=[]

    for elem in U:
        U_polys.append(galois.Poly((elem),field=GF))
    for elem in V:
        V_polys.append(galois.Poly((elem),field=GF))
    for elem in W:
        W_polys.append(galois.Poly((elem),field=GF))

    public_polys=[]
    for i in range(0, l+1): #l+1 car on inclut l on veut [0,l]
        u_i=U_polys[i](x)
        v_i=V_polys[i](x)
        w_i=W_polys[i](x)
        public_polys.append((int(beta)*u_i+int(alpha)*v_i+w_i)/gamma)
    private_polys=[]
    for i in range(l+1, m+1): # on veut [l+1,m-1]
        u_i=U_polys[i](x)
        v_i=V_polys[i](x)
        w_i=W_polys[i](x)
        private_polys.append((int(beta)*u_i+int(alpha)*v_i+w_i)/delta)
    x_power_i_t_x=[]
    for i in range(0,n-2+1):#[0,n-1]
        x_power_i_t_x.append((x**i)*t_x/delta)
    G1_alpha = multiply(G1, int(alpha))
    G1_beta = multiply(G1, int(beta))
    G1_delta = multiply(G1, int(delta))
    G1_x_power_i = [multiply(G1,int(elem)) for elem in x_power_i]
    G1_private_polys = [multiply(G1,int(elem)) for elem in private_polys]
    G1_public_polys = [multiply(G1,int(elem)) for elem in public_polys]
    G1_x_power_i_t_x = [multiply(G1,int(elem)) for elem in x_power_i_t_x]
    
    output_1=[G1_alpha, G1_beta, G1_delta, G1_x_power_i,G1_x_power_i_t_x,G1_public_polys,G1_private_polys]

    G2_beta = multiply(G2, int(beta))
    G2_gamma = multiply(G2, int(gamma))
    G2_delta = multiply(G2, int(delta))
    G2_x_power_i = [multiply(G2,int(elem)) for elem in x_power_i]

    output_2=[G2_beta, G2_gamma, G2_delta, G2_x_power_i]
    return output_1, output_2

## PROVER
def prover(U,V,W,l,sigma_1,sigma_2,a):
    print("\n============= Prover =============")
    curve_order=101

    r=GF(13)
    s=GF(17)

    m=len(U)-1
    n=len(U[0])

    G1_alpha, G1_beta, G1_delta, G1_x_power_i,G1_x_power_i_t_x,G1_public_polys,G1_private_polys = sigma_1
    G2_beta, G2_gamma, G2_delta, G2_x_power_i = sigma_2

    G1_poly=np.concatenate((G1_public_polys,G1_private_polys))

    #=================================Pour trouver t(x)  ==========================
    values = [i for i in range(1, len(U[0])+1)] # Car on a 6 colonnes
    poly_t = galois.Poly([1], field=GF)  # Start with the polynomial '1' in the given field
    for val in values:
        poly_t *= galois.Poly([1, -val], field=GF)
    t=[]
    for elem in poly_t.coeffs:
        t.append(int(elem))
    #=================================Pour trouver h(x)  ==========================
    U_polys=[]
    V_polys=[]
    W_polys=[]

    for elem in U:
        U_polys.append(galois.Poly((elem),field=GF))
    for elem in V:
        V_polys.append(galois.Poly((elem),field=GF))
    for elem in W:
        W_polys.append(galois.Poly((elem),field=GF))

    witness = a
    Ua = inner_product_polynomials_with_witness(U_polys, witness)
    Va = inner_product_polynomials_with_witness(V_polys, witness)
    Wa = inner_product_polynomials_with_witness(W_polys, witness)

    t_poly=galois.Poly(t,field=GF)
    print("t_poly(x) = ",t_poly)

    h = (Ua * Va - Wa) // t_poly
    h_rem = (Ua * Va - Wa) % t_poly
    print(h)
    print(h_rem)

    assert h_rem == 0, "h(x) is not a multiple of t(x)"
    # h_75=h(75)
    # print("h(x) = ",h_75)
    # t_75=evaluate_polynomial_galois(t, 75, GF)
    # print("t(x) = ",t_75)
    # print("h(x)*t(x) = ",h_75*t_75/GF(11))
    # print("dans G1",multiply(G1,int(h_75*t_75)))

    # print("h",h.coeffs)
    h_t_x=None
    for i in range(0, len(h.coeffs)):
        h_t_x=py_ecc.bn128.add(h_t_x,multiply(G1_x_power_i_t_x[i],int(h.coeffs[::-1][i])))
    # print("h_t_x=",h_t_x)

    #==============================================================================

    Ui_x = []

    for i in range(0, m+1):
        temp=None
        for j in range(0, len(U[i])):
            temp2=multiply(G1_x_power_i[j],int(U[i][::-1][j]))
            temp=py_ecc.bn128.add(temp,temp2)
        Ui_x.append(temp)
        
    A_1=None
    for i in range(0, m+1):
        temp=multiply(Ui_x[i],int(a[i]))
        A_1=py_ecc.bn128.add(A_1,temp)
    
    A_1=py_ecc.bn128.add(A_1,G1_alpha)
    r_delta=multiply(G1_delta,int(r))
    A_1=py_ecc.bn128.add(A_1,r_delta)
    print("A_1=",A_1)




    V_i_x_1 = []
    for i in range(0, m+1):
        temp=None
        for j in range(0, len(V[i])):
            temp2=multiply(G1_x_power_i[j],int(V[i][::-1][j]))
            temp=py_ecc.bn128.add(temp,temp2)
        V_i_x_1.append(temp)

    V_i_x_2 = []
    for i in range(0, m+1):
        temp=None
        for j in range(0, len(V[i])):
            temp2=multiply(G2_x_power_i[j],int(V[i][::-1][j]))
            temp=py_ecc.bn128.add(temp,temp2)
        V_i_x_2.append(temp)

    B_1=None
    for i in range(0, m+1):
        temp=multiply(V_i_x_1[i],int(a[i]))
        B_1=py_ecc.bn128.add(B_1,temp)
    B_1=py_ecc.bn128.add(B_1,G1_beta)
    s_delta=multiply(G1_delta,int(s))
    B_1=py_ecc.bn128.add(B_1,s_delta)
    print("B_1=",B_1)

    B_2=None
    for i in range(0, m+1):
        temp=multiply(V_i_x_2[i],int(a[i]))
        B_2=py_ecc.bn128.add(B_2,temp)
    B_2=py_ecc.bn128.add(B_2,G2_beta)
    multiply_r_s_delta=multiply(G2_delta,int(s))
    B_2=py_ecc.bn128.add(B_2,multiply_r_s_delta)
    print("B_2=",B_2)

    C_1=None
    # print("=========init========")
    # print("ht(x)_G1",h_t_x)
    # print("priv",G1_private_polys)
    # print("pub",G1_public_polys)
    # print("s", s)
    # print("r",r)
    for i in range(l+1, m+1):
        # print("i=",i,"a[i]=",a[i],"G1_poly[i]=",G1_poly[i])
        temp=multiply(G1_poly[i],int(a[i]))
        C_1=py_ecc.bn128.add(C_1,temp)
    # print("c_1 après for :",C_1)
    C_1=py_ecc.bn128.add(C_1,h_t_x)
    multiply_A_s=multiply(A_1,int(s))
    # print("A_1=",A_1)
    # print("s:",s)
    # print("multiply_A_s=",multiply_A_s)
    multiply_B_r=multiply(B_1,int(r))
    # print("multiply_B_r=",multiply_B_r)
    rs=r*s
    multiply_r_s_delta=multiply(neg(G1_delta),int(rs))
    # print("multiply_r_s_delta=",multiply_r_s_delta)

    C_1=py_ecc.bn128.add(C_1,multiply_A_s)
    C_1=py_ecc.bn128.add(C_1,multiply_B_r)
    C_1=py_ecc.bn128.add(C_1,multiply_r_s_delta)
    print("C_1=",C_1)

    return (A_1, B_2, C_1)

## VERIFIER

def verifier(pi,a,sigma_2,sigma_1,l):
    print("\n============= Verifier =============")

    A_1, B_2, C_1 = pi

    G2_beta, G2_gamma, G2_delta, G2_x_power_i = sigma_2
    G1_alpha, G1_beta, G1_delta, G1_x_power_i,G1_x_power_i_t_x,G1_public_polys,G1_private_polys = sigma_1
    
    lhs = pairing(B_2, A_1) #A_1*B_2
    print("lhs", lhs)

    D=None
    for i in range(0, l+1):
        temp=multiply(G1_public_polys[i],int(a[i]))
        D=py_ecc.bn128.add(D,temp)

    # print("D=",D)

    rhs_1 = pairing(G2_beta,G1_alpha)
    # print("rhs_1 beta_alpha =",rhs_1)
    rhs_2 = pairing(G2_gamma,D)
    # print("rhs_2 gamma_sum=",rhs_2)   
    rhs_3 = pairing(G2_delta,C_1)
    # print("rhs_3 delta_C=",rhs_3)

    rhs=rhs_1*rhs_2*rhs_3
    return lhs == rhs
    # print(" ")
    # print("lhs=",lhs)
    # print("rhs_produit=",rhs)
    # print("produit:",lhs == rhs)
    # print(" ")
    # print("rhs_somme=",rhs_1+rhs_2+rhs_3)
    # print("somme:",lhs == rhs_1+rhs_2+rhs_3)

U=np.array(U)
V=np.array(V)
W=np.array(W)

# print("U=",U,"\n")
# print("V=",V,"\n")
# print("W=",W,"\n")

#a=[1, 135, 5, 25, 125, 130] 
a = [1, 553, 5, 25, 125, 375, 125, 50]
a=np.array(a) % p
a=GF(a)

l=1 # car dans a=[1, 135, 5, 25, 125, 130] on donne en public les 2 premiers éléments de a et le reste c'est privée
sigma_1,sigma_2= trusted_setup(U,V,W,l)

G1_alpha, G1_beta, G1_delta, G1_x_power_i, G1_x_power_i_t_x, G1_public_polys, G1_private_polys = sigma_1
G2_beta, G2_gamma, G2_delta, G2_x_power_i = sigma_2

# print("dim :",len(G1_alpha)," | G1_alpha=",G1_alpha)
# print("dim :",len(G1_beta)," | G1_beta=",G1_beta)
# print("dim :",len(G1_delta)," | G1_delta=",G1_delta)
# print("dim :",len(G1_x_power_i)," | G1_x_power_i=",G1_x_power_i)
# print("dim :",len(G1_x_power_i_t_x)," | G1_x_power_i_t_x=",G1_x_power_i_t_x)
# print("dim :",len(G1_public_polys)," | G1_public_polys=",G1_public_polys)
# print("dim :",len(G1_private_polys)," | G1_private_polys=",G1_private_polys)

# print("dim :",len(G2_beta)," | G2_beta=",G2_beta)
# print("dim :",len(G2_gamma)," | G2_gamma=",G2_gamma)
# print("dim :",len(G2_delta)," | G2_delta=",G2_delta)
# print("dim :",len(G2_x_power_i)," | G2_x_power_i=",G2_x_power_i)

pi=prover(U,V,W,l,sigma_1,sigma_2,a)
isTrue=verifier(pi,a,sigma_2,sigma_1,l)
print(isTrue)

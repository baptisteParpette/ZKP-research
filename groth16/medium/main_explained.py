import zktool as zk
import numpy as np
import galois
from py_ecc.bn128 import curve_order
import galois
import numpy as np

p=curve_order #p=21888242871839275222246405745257275088548364400416034343698204186575808495617
GF = galois.GF(p) 

print("=================== GROTH16 IMPLEMENTATION ===================")

eq_input = input("Enter the equation (ex: x^3 + x + 5):") 
print("Equation: ", eq_input, "\n")

equations, solution_array = zk.decompose_polynomial(eq_input)

print("Arithmetic circuit modeling:")
for equation in equations:
    print(equation)

print("\nSet of variables =", solution_array)

L, R, O = zk.generate_r1cs(equations, solution_array)

print("L=")
for line in L:
    print(line)
print(" ")

print("R=")
for line in R:
    print(line)
print(" ")

print("O=")
for line in O:
    print(line)
print(" ")

num_eq = len(L)

# Convert the matrices to be convertible in GF (each value is brought between [0, p-1])
# Convert the matrices into Galois matrices
L_galois = GF(np.array(L) % p)
R_galois = GF(np.array(R) % p)
O_galois = GF(np.array(O) % p)

U = []
V = []
W = []
for i in range(len(solution_array)):
    U.append(zk.interpolate_lagrange(L_galois[:, i], GF, num_eq))
    V.append(zk.interpolate_lagrange(R_galois[:, i], GF, num_eq))
    W.append(zk.interpolate_lagrange(O_galois[:, i], GF, num_eq))

print("Matrix U:")
for line in U:
    print(line)

print("\nMatrix V:")
for line in V:
    print(line)

print("\nMatrix W:")
for line in W:
    print(line)

values = {"x": 5}
a = zk.compute_solution_vector(solution_array, equations, values)
a = np.array(a) % p

print("\nSolution Vector:", a)
print("Vector with variable", solution_array)

zk.init(GF)

U = np.array(U)
V = np.array(V)
W = np.array(W)

a = GF(a)
l = 1 # Publicly provide the first 2 elements of a, the rest is private
sigma_1, sigma_2 = zk.trusted_setup(U, V, W, l)
pi = zk.prover(U, V, W, l, sigma_1, sigma_2, a)
isTrue = zk.verifier(pi, a, sigma_2, sigma_1, l)
print(isTrue)
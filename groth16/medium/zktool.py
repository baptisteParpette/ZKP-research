import numpy as np
import galois
from functools import reduce
import py_ecc.bn128
from py_ecc.bn128 import G1, G2, multiply, curve_order, neg, pairing, Z1, Z2

GF = ""

def init(gf):
    global GF
    GF = gf

def decompose_polynomial(poly):
    # Replace minus signs with a '+' followed by the negative sign for splitting
    terms = poly.replace("-", "+-").split('+')

    # Normalize terms to ensure x^1 is written as x, x^0 as a constant
    terms = [t.strip().replace('x^1', 'x') for t in terms]

    equations = []
    counter = 1
    result = "result"
    result_is_zero = True

    def add_equation(lhs, rhs):
        nonlocal counter
        eq_name = f"v{counter}"
        equations.append(f"{eq_name} = {lhs} + {rhs}")
        counter += 1
        return eq_name

    def get_power_name():
        nonlocal counter
        name = f"v{counter}"
        counter += 1
        return name

    for term in terms:
        if 'x' in term:
            if '^' in term:
                coeff, power = term.split('x^')
                coeff = int(coeff) if coeff else 1
                power = int(power)
            else:
                coeff = term.split('x')[0]
                if coeff == "-":
                    coeff = -1
                else:
                    coeff = int(coeff) if coeff else 1
                power = 1

            current_x_power = "x"
            for i in range(2, power+1):
                new_power = get_power_name()
                equations.append(f"{new_power} = {current_x_power} * x")
                current_x_power = new_power

            if coeff != 1:
                coeff_power = get_power_name()
                equations.append(f"{coeff_power} = {coeff} * {current_x_power}")
                current_x_power = coeff_power

            if not result_is_zero:
                result = add_equation(result, current_x_power)
            else:
                result = current_x_power
                result_is_zero = False

        else:
            # For constant terms, simply add
            if not result_is_zero:
                result = add_equation(result, term.strip())
            else:
                result = term.strip()
                result_is_zero = False

    equations[-1] = f"out = {' '.join(equations[-1].split()[2:])}"

    words = []
    for equation in equations:
        tokens = equation.split()
        for token in reversed(tokens):
            if token.isnumeric() or (token.startswith("-") and token[1:].isnumeric()):
                words.append('1')
            elif token not in ["+", "*", "=", "-", "/"]:  # if the token is not a mathematical operator
                words.append(token)

    unique_words = []
    for elem in words:
        if elem not in unique_words:
            unique_words.append(elem)
    # Ensure '1' and 'out' are in the list and move them to indexes 0 and 1 respectively
    if '1' in unique_words:
        unique_words.remove('1')
        unique_words.insert(0, '1')
    if 'out' in unique_words:
        unique_words.remove('out')
        unique_words.insert(1, 'out')

    return (equations, list(unique_words))

def interpolate_lagrange(col, GF, num_eq):
    xs = GF(np.array([i for i in range(1, num_eq+1)]))
    poly = galois.lagrange_poly(xs, col)

    poly_return = np.pad(poly.coeffs, (max(num_eq - len(poly.coeffs), 0), 0), 'constant') #To have vectors of the same size
    return poly_return

def get_position_vector(unique_words, elements):
    # Ensure elements is a list
    if not isinstance(elements, list):
        elements = [elements]

    # Create a zero-filled list of length equal to unique_words
    vector = [0] * len(unique_words)

    for element in elements:
        # Attempt to convert the element to an integer, default to 1 if not possible
        try:
            value = int(element)
            element = '1'
        except ValueError:
            value = 1

        # Update the position in the vector by adding the deduced value if the element is in unique_words
        if element in unique_words:
            vector[unique_words.index(element)] += value

    return vector

def generate_r1cs(equations, ref_array):
    L = []
    R = []
    O = []
    for eq in equations:
        eq_split = eq.split()

        if eq_split[3] == '*':
            vecta = get_position_vector(ref_array, eq_split[2])
            L.append(vecta)
            vectb = get_position_vector(ref_array, eq_split[4])
            R.append(vectb)
            vectc = get_position_vector(ref_array, eq_split[0])
            O.append(vectc)

        if eq_split[3] == '+':
            if "out" in eq:
                list_var = eq_split[2:]
            else:
                list_var = [eq_split[2], eq_split[4]]
            vecta = get_position_vector(ref_array, list_var)
            L.append(vecta)
            vectb = get_position_vector(ref_array, "1")
            R.append(vectb)
            vectc = get_position_vector(ref_array, eq_split[0])
            O.append(vectc)

    return (L, R, O)

def evaluate_expression(expr, values_dict):
    terms = expr.split()
    if '+' in terms:
        idx = terms.index('+')
        left_expr = " ".join(terms[:idx])
        right_expr = " ".join(terms[idx+1:])
        left_val = evaluate_expression(left_expr, values_dict)
        right_val = evaluate_expression(right_expr, values_dict)
        if isinstance(left_val, str):
            return left_val + " + " + str(right_val)
        elif isinstance(right_val, str):
            return str(left_val) + " + " + right_val
        else:
            return left_val + right_val
    elif '*' in terms:
        idx = terms.index('*')
        left_expr = " ".join(terms[:idx])
        right_expr = " ".join(terms[idx+1:])
        left_val = evaluate_expression(left_expr, values_dict)
        right_val = evaluate_expression(right_expr, values_dict)
        if isinstance(left_val, str):
            return left_val + " * " + str(right_val)
        elif isinstance(right_val, str):
            return str(left_val) + " * " + right_val
        else:
            return left_val * right_val
    else:
        if terms[0] in values_dict:
            return values_dict[terms[0]]
        elif terms[0].isnumeric():
            return int(terms[0])  # Convert string number to integer
        else:
            return expr



def compute_solution_vector(unique_words, equations, values):
    values_dict = {'1': 1}
    values_dict.update(values)

    unresolved_equations = equations.copy()

    while unresolved_equations:
        newly_resolved = []

        for equation in unresolved_equations:
            lhs, rhs = equation.split("=")
            lhs = lhs.strip()
            rhs_value = evaluate_expression(rhs.strip(), values_dict)

            if not isinstance(rhs_value, str):  # if the evaluation is successful
                values_dict[lhs] = rhs_value
                newly_resolved.append(equation)
            else:
                print(f"{lhs} remains unresolved.")

        if not newly_resolved:  # if no new equations were resolved in this pass
            print("Cannot resolve:", unresolved_equations)
            break

        for equation in newly_resolved:
            unresolved_equations.remove(equation)

    return [values_dict.get(word, 0) for word in unique_words]


def evaluate_polynomial_galois(coefs, x, GF):
    result = GF(0)
    for coef in coefs:
        result = result * x + GF(coef)
    return int(result)

def inner_product_polynomials_with_witness(polys, witness):
        mul_ = lambda x, y: x * y
        sum_ = lambda x, y: x + y
        return reduce(sum_, map(mul_, polys, witness))

def trusted_setup(U,V,W,l):
 
    m=len(U)-1
    n=len(U[0])

    #========================== Pour trouver t(x)  ==========================
    values = [i for i in range(1, len(U[0])+1)]
    poly_t = galois.Poly([1], field=GF)
    for val in values:
        poly_t *= galois.Poly([1, -val], field=GF)
    t=[]
    for elem in poly_t.coeffs:
        t.append(int(elem))
    #=========================================================================
    
    x=GF(75)
    print("x = ",int(x))

    t_x=evaluate_polynomial_galois(t, x, GF)

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

    Ua = inner_product_polynomials_with_witness(U_polys, a)
    Va = inner_product_polynomials_with_witness(V_polys, a)
    Wa = inner_product_polynomials_with_witness(W_polys, a)

    t_poly=galois.Poly(t,field=GF)

    h = (Ua * Va - Wa) // t_poly
    h_rem = (Ua * Va - Wa) % t_poly

    assert h_rem == 0, "h(x) is not a multiple of t(x)"
    h_t_x=None
    for i in range(0, len(h.coeffs)):
        h_t_x=py_ecc.bn128.add(h_t_x,multiply(G1_x_power_i_t_x[i],int(h.coeffs[::-1][i])))

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

    B_2=None
    for i in range(0, m+1):
        temp=multiply(V_i_x_2[i],int(a[i]))
        B_2=py_ecc.bn128.add(B_2,temp)
    B_2=py_ecc.bn128.add(B_2,G2_beta)
    multiply_r_s_delta=multiply(G2_delta,int(s))
    B_2=py_ecc.bn128.add(B_2,multiply_r_s_delta)
    print("B_2=",B_2)

    C_1=None
    for i in range(l+1, m+1):
        temp=multiply(G1_poly[i],int(a[i]))
        C_1=py_ecc.bn128.add(C_1,temp)
    C_1=py_ecc.bn128.add(C_1,h_t_x)
    multiply_A_s=multiply(A_1,int(s))
    multiply_B_r=multiply(B_1,int(r))
    rs=r*s
    multiply_r_s_delta=multiply(neg(G1_delta),int(rs))

    C_1=py_ecc.bn128.add(C_1,multiply_A_s)
    C_1=py_ecc.bn128.add(C_1,multiply_B_r)
    C_1=py_ecc.bn128.add(C_1,multiply_r_s_delta)
    print("C_1=",C_1)

    return (A_1, B_2, C_1)

def verifier(pi,a,sigma_2,sigma_1,l):
    print("\n============= Verifier =============")

    A_1, B_2, C_1 = pi

    G2_beta, G2_gamma, G2_delta, G2_x_power_i = sigma_2
    G1_alpha, G1_beta, G1_delta, G1_x_power_i,G1_x_power_i_t_x,G1_public_polys,G1_private_polys = sigma_1
    
    lhs = pairing(B_2, A_1)

    D=None
    for i in range(0, l+1):
        temp=multiply(G1_public_polys[i],int(a[i]))
        D=py_ecc.bn128.add(D,temp)

    rhs_1 = pairing(G2_beta,G1_alpha)
    rhs_2 = pairing(G2_gamma,D)
    rhs_3 = pairing(G2_delta,C_1)

    rhs=rhs_1*rhs_2*rhs_3
    return lhs == rhs


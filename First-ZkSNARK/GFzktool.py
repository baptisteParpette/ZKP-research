import numpy as np
import matplotlib.pyplot as plt
import galois

def decompose_polynomial(poly):
    # Replace minus signs with a '+' followed by the negative sign for splitting
    terms = poly.replace("-", "+-").split('+')
    
    # Normalize terms to make sure x^1 is written as x, x^0 is written as a constant
    terms = [t.strip().replace('x^1', 'x') for t in terms]
    
    equations = []
    counter = 1
    result = "result"
    result_is_zero = True
    
    def add_equation(lhs, rhs):
        nonlocal counter
        eq_name = f"equation_{counter}"
        equations.append(f"{eq_name} = {lhs} + {rhs}")
        counter += 1
        return eq_name

    def get_power_name():
        nonlocal counter
        name = f"power_{counter}"
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
            # If just a constant term, simply add
            if not result_is_zero:
                result = add_equation(result, term.strip())
            else:
                result = term.strip()
                result_is_zero = False

    return equations

def get_unique_words(equations):
    words = set()
    for equation in equations:
        tokens = equation.split()
        for token in tokens:
            if token.isnumeric() or (token.startswith("-") and token[1:].isnumeric()):  
                words.add('1')
            elif token not in ["+", "*", "=", "-", "/"]:  # if the token is not a mathematical operator
                words.add(token)
    return words

def get_position_vector(unique_words, elements):
    # Make sure elements is a list
    if not isinstance(elements, list):
        elements = [elements]
    
    # Create a list of length of unique_words with all zeros
    vector = [0] * len(unique_words)
    
    for element in elements:
        # Try to convert the element to an integer. If it's not an integer, default value is 1.
        try:
            value = int(element)
            element = '1'
        except ValueError:
            value = 1
        
        # If the element is in unique_words, update its position in the vector by adding the deduced value
        if element in unique_words:
            vector[unique_words.index(element)] += value
    
    return vector

def lagrange_basis_mod(j, x_vals, mod=41):
    """Returns the j-th Lagrange basis polynomial for the given x values using modular arithmetic."""
    n = len(x_vals)
    basis_coeffs = [1]  # Start with a polynomial "1"
    for m in range(n):
        if m != j:
            # Compute the numerator and denominator for the basis polynomial factors
            numerator_coeffs = [1, sub_mod(0, x_vals[m], mod)]
            denominator = sub_mod(x_vals[j], x_vals[m], mod)
            # Multiply the current term by the new factor (using modular multiplication)
            term_coeffs = [mul_mod(coeff, pow_mod(denominator, mod - 2, mod), mod) for coeff in numerator_coeffs]
            basis_coeffs = np.polymul(basis_coeffs, term_coeffs) % mod
    return np.poly1d(basis_coeffs)

def lagrange_interpolation_mod(y_vals, mod=41):
    """Returns the Lagrange interpolating polynomial for the given y values using modular arithmetic."""
    x_vals = range(1, len(y_vals) + 1)
    polynomial_coeffs = [0]  # Start with polynomial "0"
    for j in range(len(y_vals)):
        # Multiply the y value with the corresponding Lagrange basis polynomial (using modular multiplication)
        basis_poly = lagrange_basis_mod(j, x_vals, mod)
        term_coeffs = (basis_poly.coeffs * y_vals[j]) % mod
        polynomial_coeffs = np.polyadd(polynomial_coeffs, term_coeffs) % mod
    return np.poly1d(polynomial_coeffs)

def interpolate_and_get_coeff_matrix_mod(matrix, mod=41):
    """Interpolate each row of the matrix and return the matrix of polynomial coefficients using modular arithmetic."""
    interpolated_polynomials = []
    for row in matrix:
        interpolated_polynomials.append(lagrange_interpolation_mod(row, mod))
        
    max_degree = max(len(p.coeffs) for p in interpolated_polynomials) - 1
    coeff_matrix = []
    for p in interpolated_polynomials:
        # Pad coefficients to have the same length (using modular addition)
        coeffs = np.pad(p.coeffs, (0, max_degree - len(p.coeffs) + 1), 'constant', constant_values=0) % mod
        coeff_matrix.append(coeffs)
    
    return np.array(coeff_matrix)

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
                print(f"{lhs} = {rhs_value}")
            else:
                print(f"{lhs} remains unresolved.")
                
        if not newly_resolved:  # if no new equations were resolved in this pass
            print("Cannot resolve:", unresolved_equations)
            break

        for equation in newly_resolved:
            unresolved_equations.remove(equation)
            
    return [values_dict.get(word, 0) for word in unique_words]


def polynomial_dot_product(poly_matrix, solution_vector):
    """
    Calculate the dot product between a polynomial represented by a matrix 
    and a solution vector.

    Parameters:
    - poly_matrix (np.array): A 2D numpy array representing the polynomial. 
                              Each row corresponds to a term in the polynomial 
                              and each column to a power of x.
    - solution_vector (list): A list of numerical solutions.

    Returns:
    - np.array: A 1D numpy array representing the result of the dot product 
                of the polynomial and the solution vector.
    """
    # Ensure the inputs are numpy arrays.
    poly_matrix = np.array(poly_matrix)
    solution_vector = np.array(solution_vector)
    
    # Calculate the dot product for each term of the polynomial.
    result = np.dot(solution_vector,poly_matrix)
    
    # Invert the result.
    result = np.flip(result)
    
    return result

def polynomial_coefficients(n):
    """
    Compute the coefficients of the polynomial (x - 1) * (x - 2) * ... * (x - n).
    
    Parameters:
    - n (int): The number of terms in the polynomial.

    Returns:
    - np.array: An array representing the coefficients of the polynomial.
    """
    # Initialize the polynomial to be just "x - 1"
    poly = np.array([1, -1])

    # Convolve successively with (x - 2), (x - 3), ... , (x - n)
    for i in range(2, n + 1):
        poly = np.convolve(poly, [1, -i])

    # Reverse the order to match the desired output
    return poly[::-1]

def is_remainder_close_to_zero(remainder, tolerance=1e-5):
    """
    Check if the remainder is close to zero within a certain tolerance.

    Parameters:
    - remainder (np.array): The remainder from polynomial division.
    - tolerance (float): The threshold below which values are considered zero.

    Returns:
    - bool: True if the remainder is close to zero, False otherwise.
    """
    return np.all(np.abs(remainder) < tolerance)


def polynomial_division(T, Z):
    """
    Divide polynomial T by polynomial Z and print the quotient and remainder.

    Parameters:
    - T (np.array): Polynomial coefficients of the dividend.
    - Z (np.array): Polynomial coefficients of the divisor.
    """
    quotient, remainder = np.polydiv(T, Z)
    return quotient, remainder

def plot_polynomials(coefficients_list,xlim=[-10,10],ylim=[-10,10]):
    """
    Affiche graphiquement les polynômes à partir de leurs coefficients.
    
    :param coefficients_list: Une liste de listes où chaque sous-liste contient les coefficients d'un polynôme.
                              Par exemple, [[1, 2, 3], [3, 2]] représenterait les polynômes x^2 + 2x + 3 et 3x + 2.
    """
    # Plage de valeurs x pour l'affichage
    x = np.linspace(xlim[0], xlim[1], 400)
    
    plt.figure(figsize=(10, 6))
    
    # Parcourir chaque liste de coefficients et tracer le polynôme correspondant
    for idx, coeffs in enumerate(coefficients_list):
            y = np.polyval(coeffs, x)
            
            # Trouver les racines du polynôme
            roots = np.roots(coeffs)
            formatted_roots = ", ".join([f"{root:.2f}" for root in roots if np.isreal(root)])
            
            plt.plot(x, y, label=f'Polynôme {idx + 1} (Racines: {formatted_roots})')
        
    plt.title("Graphique des polynômes avec leurs racines")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    plt.legend()
    plt.show()

def add_mod(a, b, mod=41):
    return (a + b) % mod

def sub_mod(a, b, mod=41):
    return (a - b) % mod

def mul_mod(a, b, mod=41):
    return (a * b) % mod

def pow_mod(a, b, mod=41):
    return pow(a, b, mod)

# Pour la division, on utilise l'inverse modulaire
def inv_mod(a, mod=41):
    # L'inverse modulaire n'existe que si a et mod sont premiers entre eux
    return pow(a, mod - 2, mod)

def div_mod(a, b, mod=41):
    b_inv = inv_mod(b, mod)
    return mul_mod(a, b_inv, mod)


    
   
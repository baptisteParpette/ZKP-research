import sympy
import random

# Trouver un générateur g qui a un ordre q dans le groupe modulo p
def find_generator(p, q):
    for candidate in range(2, p):
        if pow(candidate, q, p) == 1 and candidate % p != 1:
            return candidate
    raise ValueError("No generator found")



# Générer un grand nombre premier sûr pour q en utilisant une méthode différente
def find_safe_prime(bits=128):
    q = sympy.randprime(2**(bits-1), 2**bits)
    p = 2*q + 1
    while not sympy.isprime(p):
        q = sympy.randprime(2**(bits-1), 2**bits)
        p = 2*q + 1
    return p, q

p, q = find_safe_prime()


# Vérifier que p et q sont premiers
assert sympy.isprime(p) and sympy.isprime(q)

# Choisir un générateur pour le groupe. Pour un nombre premier sûr, 2 est souvent un générateur.
g = find_generator(p, q)

def schnorr_protocol(repetitions=10):
    valid_count = 0
    
    for _ in range(repetitions):
        # Données du prouveur
        s = random.randint(1, q-1)  # Secret du prouveur
        v = pow(g, s, p)            # Clé publique

        # Étape d'engagement
        r = random.randint(1, q-1)  
        R = pow(g, r, p)

        # Étape de challenge
        c = random.randint(1, q-1)

        # Étape de réponse
        a = (r - c * s) % q

        # Étape de vérification
        verification = (pow(g, a, p) * pow(v, c, p)) % p
        if verification == R:
            #print("Tous les parametres sont :", p, q, g, s, v, r, R, c, a, verification, sep='\n')
            valid_count += 1

    return valid_count == repetitions

print(schnorr_protocol())
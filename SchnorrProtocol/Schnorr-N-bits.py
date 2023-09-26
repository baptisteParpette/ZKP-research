import random
from sympy import isprime
from tqdm import tqdm

def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        if isprime(p):
            return p

def generate_group(bits):
    """Générer un groupe basé sur un nombre premier de 'bits' bits."""
    q = generate_prime(bits)
    p = 2*q + 1
    while not isprime(p):
        q = generate_prime(bits)
        p = 2*q + 1
    return p, q

def find_generator(p, q):
    while True:
        g = random.randint(2, p - 2)
        if pow(g, q, p) == 1 and g > 1:
            return g

def schnorr_protocol(bits):
    # Génération des paramètres
    p, q = generate_group(bits)
    g = find_generator(p, q)

    # Clés du prouveur
    x = random.randrange(1, q)
    y = pow(g, x, p)

    print(f"p = {p}, q = {q}, g = {g}")
    print(f"Clé secrète (x) du prouveur : {x}")
    print(f"Clé publique (y) du prouveur : y = g^x mod p = {y}\n")

    # Prouveur: Étape d'engagement
    v = random.randrange(1, q)
    t = pow(g, v, p)
    print(f"Prouveur choisit aléatoirement v = {v}")
    print(f"Prouveur calcule t = g^v mod p = {t} et l'envoie au vérificateur.\n")

    # Vérificateur: Étape de défi
    c = random.randrange(1, q)
    print(f"Vérificateur choisit aléatoirement c = {c} et l'envoie au prouveur.\n")

    # Prouveur: Étape de réponse
    r = (v - c*x) % q
    print(f"Prouveur calcule r = v - c*x mod q = {r} et l'envoie au vérificateur.\n")

    # Vérificateur: Étape de vérification
    print(f"Vérificateur vérifie si g^r * y^c mod p est égal à t.")
    if (pow(g, r, p) * pow(y, c, p)) % p == t:
        print(f"{pow(g, r, p)} * {pow(y, c, p)} mod {p} = {t}")
        print("La preuve est valide!\n")
    else:
        print("La preuve n'est pas valide.\n")

# Choisissez le nombre de bits ici.
bits = 5  # À remplacer par le nombre de bits souhaité (par exemple 50)
schnorr_protocol(bits)

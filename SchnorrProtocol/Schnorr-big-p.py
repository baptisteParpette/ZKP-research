from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.backends import default_backend
from tqdm import tqdm
import random

def find_generator(p, q, backend):
    """Trouver un générateur pour le groupe mod p."""
    for _ in range(100):  # Tentatives pour trouver un générateur
        h = random.randrange(2, p - 2)
        g = pow(h, (p - 1) // q, p)
        if g > 1:
            return g
    raise ValueError("Cannot find a generator")

# Générer un grand nombre premier pour DSA (Digital Signature Algorithm)
parameters = dsa.generate_parameters(key_size=1024, backend=default_backend())


p = parameters.parameter_numbers().p
q = parameters.parameter_numbers().q

g = find_generator(p, q, default_backend())

print(f"p = {p}")
print(f"q = {q}")
print(f"g = {g}\n")

# Clés du prouveur
x = random.randrange(1, q)
y = pow(g, x, p)
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

# # Vérificateur tente de trouver le secret x
# print("Vérificateur tente de trouver le secret x...")
# # Avant de commencer la boucle, initialise la barre de progression
# pbar = tqdm(total=q, desc="Recherche de x", position=0, leave=True)

# i = 1
# try:
#     while i < q:
#         if pow(g, i, p) == y:
#             print(f"\nLe vérificateur a trouvé le secret : x = {i}")
#             break
#         i += 1
#         pbar.update(1)
# except KeyboardInterrupt:
#     # Si l'utilisateur veut interrompre la boucle manuellement
#     pbar.close()
#     print("\nRecherche interrompue par l'utilisateur.")

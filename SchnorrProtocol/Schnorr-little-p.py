import random
from sympy import isprime

def find_generator(p):
    """Trouver un générateur pour le groupe mod p."""
    for g in range(2, p):
        if pow(g, p-1, p) == 1 and pow(g, (p-1)//2, p) != 1:
            return g
    return None

# Paramètres
p = 23  # Un nombre premier (pour la simplicité)
g = find_generator(p)
print(f"Le nombre premier choisi est p = {p} et son générateur est g = {g}.\n")

x = random.randint(1, p-2)  # Clé secrète
y = pow(g, x, p)  # Clé publique
print(f"Clé secrète (x) du prouveur : {x}")
print(f"Clé publique (y) du prouveur : y = g^x mod p = {y}\n")

# Prouveur: Étape d'engagement
v = random.randint(1, p-2)
t = pow(g, v, p)
print(f"Prouveur choisit aléatoirement v = {v}")
print(f"Prouveur calcule t = g^v mod p = {t} et l'envoie au vérificateur.\n")

# Vérificateur: Étape de défi
c = random.randint(1, p-2)
print(f"Vérificateur choisit aléatoirement c = {c} et l'envoie au prouveur.\n")

# Prouveur: Étape de réponse
r = (v - c*x) % (p-1)
print(f"Prouveur calcule r = v - c*x mod (p-1) = {r} et l'envoie au vérificateur.\n")

# Vérificateur: Étape de vérification
print(f"Vérificateur vérifie si g^r * y^c mod p est égal à t.")
if pow(g, r, p) * pow(y, c, p) % p == t:
    print(f"{pow(g, r, p)} * {pow(y, c, p)} mod {p} = {t}")
    print("La preuve est valide!\n")
else:
    print("La preuve n'est pas valide.\n")

# Vérificateur tente de trouver le secret x
print("Vérificateur tente de trouver le secret x...\n")
for i in range(1, p-1):
    if pow(g, i, p) == y:
        print(f"Le vérificateur a trouvé le secret : x = {i}")
        break

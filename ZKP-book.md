# Preuves à divulgation nulle de connaissance (ZKP)

Les preuves à divulgation nulle de connaissances (Zero Knowledge Proofs) couvrent un concept spécifique dans le domaine de la cryptographie. Elles permettent à une partie ; le **prouveur** ; de montrer à une autre partie ; le **vérifieur** ; qu'une **affirmation** est vraie, sans révéler d'information supplémentaire ; elle reposent également sur un **tiers de confiance** qui défini l'espace de travail de la preuve.

### Exemples simples

Exemple 1 (Où est Charlie ?)
---------
Dans le jeu "où est Charlie ?", il faut retrouver les coordonnées d'un personnage appelé Charlie dans un dessin rempli de détails. Dans la solution de base, le prouveur est celui qui indique où est le personnage, le vérifieur peut voir sur le dessin que Charlie est au bon endroit indiqué. Le tiers de confiance peut être vu comme une personne qui garantie au vérifier que Charlie est bien présent quelque part sur l'image ou que l'image n'a pas été remplacée.

Dans une approche ZKP le prouveur peut montrer au vérifieur qu'il sait où se trouve Charlie sans divulguer sa position.

Pour cela, il recouvre l'image d'un cache noir largement plus grand que le dessin. C'est à dire au moins 3 fois la dimension de l'image sur ses deux dimensions. Dans ce cache, un trou est fait de la dimension du personnage de Charlie et positionne ce trou sur "l'image de Charlie". Le cache recouvre largement l'image et ne divulgue que Charlie, mais pas sa position dans l'image. Le cache couvrant les coordonnées de l'image. Le vérifieur voit charly à travers le trou, mais ne sait pas à quelles coordonnées dans l'image il se trouve. En repartant le vérifieur sais que le prouveur à trouvé Charlie, mais le vérifieur ne sais pas où il se trouve. Il y a eu preuve de l'affirmation sans divulgation de la coordonnée.

Exemple 2 (Résolution de sudoku)
---------
Le jeu de sudoku consiste à répartir des chiffres de 1 à 9 dans une grille 9x9 formée de 9 pavés de 3x3. Pour être résolue la grille doit comporter tous les chiffres uniques de 1 à 9 sur toutes les lignes, toutes les colonnes et tous les pavés de 9 cases. Pour contraindre le système, la grille est initialement peuplée de valeurs qui par déduction amènent à une solution unique. Le jeu consiste à répartir les 27 séries de 9 valeurs de toutes les zones de la grille (lignes, colonnes, pavés). Dans la solution de base, le prouveur est celui qui montre que tous les chiffres sont présents et répartis dans la grille.

Dans une approche ZKP, le prouveur peut montrer au vérifieur qu'il connait la solution sans divulguer la répartition des chiffres.

Pour cela, il ne marque pas la solution directement sur la grille, mais sur des étiquettes mobiles qu'il colle sur les cases vides de la grilles. Chaque case contient une étique avec la valeur solution. Ces étiquettes sont retournée afin que le vérifieur ne puisse pas voir les valeurs solution. Pour que la preuve ZKP fonctionne, le vérifieur pose 18  questions. Chaque question consiste à demander l'ensemble des étiquettes constituant une des zone de répartition (ligne, colonne ou pavé). Le prouveur prend les étiquettes les mélange caché et dévoile au vérifieur que les 9 chiffres sont bien présents de manière unique. Puis il replace les étiquettes face cachées sur leur emplacement. En répétant ce processus 18 fois, le vérifier est convaincu à 100% que le prouver connait bien la solution à la grille, mais le vérifier ne connait pas la position des différentes valeurs dans la grille.

Cette preuve est dite interactive, car elle peut se terminer avant la fin des 18 intérations. En effet, au fur et à mesure des itérations le vérifier devient de plus en plus convaincu que le prouver a bien résolu la grille.

Ces deux exemples donnent une intuition sur le principe de fonctionnement des approches par ZKP. Dans le cadre général il s'agit d'arriver à montrer qu'on connait la réponse à une question en révélant des valeurs qui n'ont pas de correlation directe avec la solution. "Charlie est là, mais je n'ai pas sa coordonnée", "les chiffres sont là mais je n'ai pas vu l'organisation".

Il existe de nombreux exemples plus ou moins intuitifs sur les méchanismes de ZKP. Dans le domaine de la crypto, les techniques tournent autour de la résolution de polynomes de degrés n. Le principe est de montrer qu'on connait la solution d'un système d'équations sachant que la complexité du système rend improbable le fait de trouver la solution par tirage aléatoire.

<!-- Par exemple, si vous savez qu'il s'agit d'un ensemble de 10 courbes, et que le prouveur annonce qu'il pense que toutes les courbes de cet ensemble passent par des points de coordonnées (12, 100), (20, 230), (32, 430), (1233,2301), (124, 131389), (1212,101281818) et (13123, 12239191281), il y a de fortes chance qu'il connaisse l'ensemble. Le mécanisme  zkSNARK consiste à construire cet ensemble de courbes afin de permettre à un prouveur qu'il connait une solution type que le verifier peut facilement controler.
Pour ceci le vérifier connait une courbe de référence publique (x-1)(x-2)(x-3).... Cette courbe coupe l'axe des x aux coordonnées (0, 1), (0, 2) (0, 3) (0, 4). D'autre part le vérifier possède un certain nombre de coefficient de courbes qui sont indirectement liés au système d'équation initial. Le prouver fourni un vecteur solution de valeurs [x1,...xn] que le vérifier peu appliquer à son système de courbe. Le vérifier peut alors controler que sa courbe publique est un diviseur exact de la courbe déduite à partir du vecteur solution appliqué au système de coefficients. -->

<!-- Le prouver indique qu'il connait une solution [x1,...xn], sans que le vérifieur puisse remonter aux courbes initiales. -->


<!-- Voici des exemples simplifier :

- Caverne l'ali baba

- Le problème du daltonien et des boulles de couleur -->

<!-- ### Applications //SFR pour moi c'est inutile pour l'instant

Les ZKP ont de nombreuses applications, notamment :

- **Authentification** : Prouver que vous connaissez un mot de passe sans le révéler.
- **Transactions privées** : Effectuer des transactions sur une blockchain sans révéler les montants ou les participants.
- **Vote électronique** : Voter sans révéler son choix, tout en prouvant que le vote a été effectué correctement.

### Définition d'un ZKP:

Pour quoi preuve soit considerer comme un ZKP, elle doit repondre à 3 propriété :

- consistance (*completeness*) : Si la proposition (statement) est vrai et que le verifieur est honnete, alors il sera forcement convaincu par un honnete prouver.

- robustesse (*soundness*) : Si la proposition est fausse et que le verifieur est honete, alors il sera impossible de le convaincre de la verasité de la proposition.

- aucun apport d'information (*zero knowledge*) : Si la propositon est vrai, il sera impossible au verifier de retrouver l'information secret.

### Comment cela fonctionne-t-il?

Sans entrer dans les détails techniques, le fonctionnement des ZKP repose sur des problèmes mathématiques complexes qui sont difficiles à résoudre sans connaître certaines informations secrètes. Le prouveur utilise ces informations secrètes pour générer une preuve, et le vérificateur peut alors vérifier cette preuve sans jamais connaître les informations secrètes. Le verifieur à la possibilité de lancer des challenges au prouver afin de se convaincre qu'il connait pas le secret.

[mettre un schema des echange dans un ZKPi]

## Les different type de ZKP

Etant donné que les regles pour definir un ZKP sont simples, il y a ensuite des categories qui se sont former avec d'autre propriete afin d'optenir des types de preuve plus adapter aux context dans lequel on les utilise.

### Interactive vs Non-Interactive

Nous avons vu dans l'introduction des ZKP que le verifier et le prouver commiquait ensemble et qu'il pouvait y avoir plusieurs allers retours possible afin d'effectué des challenge, ceci represente les ZKP interactive ou le verifier peux demander un complement de preuve sous forme de challenge. En opposition il existe des ZKP non interactif, dans ce cas de figure c'est au prouver de former une proposition suffisament évolué pour que n'importe quelle verifier honnet puisse etre convaincu directement.

Les iZKP sont possible grace à l'heuristique de Fiat-Shamir (qui se base sur la resistance de collisison des fonction de hashage) En réalité ce sont ses dernière qui sont le plus developper et mise en application, car les peuves interactive sont plus scalable

Aventage et inconveniant :

|        | Avantage                                                                                                                                             | Inconveniant                                                                                                                                                              |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ZKP-I  | Plus simples à comprendre et à mettre en œuvre<br/>Souplesse et Adaptabilité                                                                         | Besoins de communication (ce qui peut être inefficace en termes de temps et de ressources)<br/>Non transférables                                                          |
| ZKP-NI | Pas besoin d'interaction <br/>Transférabilité : La preuve peut être vérifiée par n'importe qui<br/>Meilleure efficacité pour les systèmes distribués | Complexité<br/>Taille de la preuve : Les preuves non interactives peuvent être plus grandes en taille, ce qui peut être problématique pour le stockage ou la transmission |

--------- -->

### zk-SNARK
Les zk-SNARKs sont des preuves à divulgation nulle de connaissance succinctes et non interactives. Non-interactif, veut dire que la preuve est validée en un seul échange, succcincte veut dire que le temps de calcul pour le vérifieur doit être rapide. Groth16 est un implantation du protocole sk-Snark et nous proposons ici de présenter le fonctionnement général et justifier les différentes étapes. Nous expliquerons cela sans faire appel à de trop grandes notions théoriques mathématiques, tout en illustrant de lignes de code les exemples les plus importants.

Nous donnons en annexe une liste de lecture permettant de rentrer plus facilement dans certains détails. Ce document est fortement inspiré de deux sources.

Notre objectif étant que le protocole soit compréhensible dans cette première lecture.

Dans zkSnarks, la preuve sans divulgation consiste à indiquer à un vérifier qu'on connait une polynôme sans divulguer l'équation du polynome. Partons du polynôme : f(x) = 3x^3+5x^2+10x+3 que seul le prouveur connait.

La question est la suivante, en tant que prouveur "Comment prouver à une personne que je connais ce polynôme" sans lui indiquer les coefficients (3, 5, 10, 3) ni les degrés correspondants.

Si j'indique au vérifieur les couples de valeurs : (0, 3) (1, 21), (2, 67) (3, 159), il peut alors confirmer que je connais cette courbe, car il n'y a qu'une seule courbe de degré 3 qui passe par 4 points. Mais il y a de fortes chances qu'il puisse remonter à la courbe source également. Je n'ai pas pu "cacher" la courbe. D'autre part, j'aurais pu inventer ces points de toute pièce...  En gardant le principe de divulgation de certaines coordonnées, nous avons deux challenges à résoudre : indiquer que je connais le polynôme sans en donner les coefficients afin que le vérifieur puisse vérifier qu'une courbe associée existe, masquer ces informations afin que le verifier ne puisse pas remonter au polynôme source tout en garantissant que le masqage ne me permet pas de choisir des chiffres au hasard.

Le premier challenge, consiste à transformer l'équation vers un ensemble de polynomes uniques qui possèdent la même solution que le polynme initial. Le polynôme initial est transformé dans un système d'équations qui présente le même ensemble de solutions que le polynôme initial, mais qui rend fortement improbable de remonter au polynôme source.

Cette transformation se fait en trois étapes :
  - 1) Transformation du polynôme initial dans un circuit R1CS
  - 2) Transformation du circuit en coefficients d'un système de courbe quadratique
  - 3) Extension du système de courbes quadratiques pour équilibrer les équations

# Circuit R1CS
Le circuit R1CS permet de réexprimer le polynôme initial dans un ensemble portes de calcul ne contenant que des additions et des multiplications. Pour faire simple les portes illustrent les multiplications, les passages de porte les additions.
`f(x) = 3x^3+5x^2+10x+3`

```
v1 = x * x   (1)  
v2 = x * v1  (2)  
v3 = 3 * v2  (3)  
v4 = 5 * v1  (4)  
v5 = 10 * x  (5)  
out = v3 + v4 + v5 + 3 (6)  
out = (v3 + v4 + v5 + 3) * 1 (6bis)  
```

Cette série d'opération va être représentée par une matrice contenant les coefficients de chaque opération.
Les colonnes de la matrice représentent les variables. Les lignes représentent la série d'opérations à appliquer.
Chaque opération unitaire est convertie par une ligne dans la matrice.

Les colonnes de la matrice sont donc `[ 1 out x v1 v2 v3 v4 v5 ]`.  
Le système d'équation se résume à 3 matrices, dont le résultat fourni la sortie finale : L * R = O qui signifie : la sortie Left(L) * Right(O) = Out(O).    

```
//L    
//1 out x v1 v2 v3 v4 v5  
[  
  0  0  1  0  0  0  0  0    // x  
  0  0  1  0  0  0  0  0    // x  
  3  0  0  0  0  0  0  0    // 3  
  5  0  0  0  0  0  0  0    // 5  
 10  0  0  0  0  0  0  0    // 10  
  3  0  0  0  0  1  1  1    // (6bis)  
]
```

```
//R  
//1 out x v1 v2 v3 v4 v5  
[  
  0  0  1  0  0  0  0  0  // x  
  0  0  0  1  0  0  0  0  // v1  
  0  0  0  0  1  0  0  0  // v2  
  0  0  0  1  0  0  0  0  // v1  
  0  0  1  0  0  0  0  0  // x  
  1  0  0  0  0  0  0  0  // (6bis)  
]
```

```
//out  
//1 out x v1 v2 v3 v4 v5  
[  
  0  0  0  1  0  0  0  0    // v1  
  0  0  0  0  1  0  0  0    // v2  
  0  0  0  0  0  1  0  0    // v3   
  0  0  0  0  0  0  1  0    // v4  
  0  0  0  0  0  0  0  1    // v5  
  0  1  0  0  0  0  0  0    // out  
]  
```


Le vecteur témoin est un vecteur solution de l'équation qui sera transmis au vérifieur. Il correspond aux variables internes et externes du circuit.
`w = [ 1 out x v1 v2 v3 v4 v5]` on peut prendre n'importe quelle valeur de x, et calculer alors toutes les autres valeurs. Si x = 5 alors on aura comme vecteur témoins les valeurs suivantes :  `w = [ 1 553 5 25 125 375 125 50]`  
  
Lw * Rw = Ow  
  
Que l'on peut vérifier avec le code python suivant :
```python
import numpy as np
import random

# Define the matrices
O = np.array([
[0,0,0,1,0,0,0,0],
[0,0,0,0,1,0,0,0],
[0,0,0,0,0,1,0,0],
[0,0,0,0,0,0,1,0],
[0,0,0,0,0,0,0,1],
[0,1,0,0,0,0,0,0]
])

L = np.array([
[ 0,0,1,0,0,0,0,0],
[ 0,0,1,0,0,0,0,0],
[ 3,0,0,0,0,0,0,0],
[ 5,0,0,0,0,0,0,0],
[10,0,0,0,0,0,0,0],
[ 3,0,0,0,0,1,1,1]
])

R = np.array([
[0,0,1,0,0,0,0,0],
[0,0,0,1,0,0,0,0],
[0,0,0,0,1,0,0,0],
[0,0,0,1,0,0,0,0],
[0,0,1,0,0,0,0,0],
[1,0,0,0,0,0,0,0]
])

# pick random values for x and y
x = random.randint(1,1000)
#x = 5

# this is our orignal formula
v1 = x * x
v2 = x * v1
v3 = 3 * v2
v4 = 5 * v1
v5 = 10 * x
out = v3 + v4 + v5 + 3

w = np.array([1, out, x, v1, v2, v3, v4, v5])

result = O.dot(w) == np.multiply(L.dot(w),R.dot(w))
assert result.all(), "result contains an inequality"

print("-->", w)
```

Ces matrices ne font que représenter le polynôme initial en le décomposant en une multiplication de matrice. Le polynôme va maintenant être masqué dans un système d'équation quadratiques, constitué d'autant de courbes quadratique que de paramètres de l'équation, et pour lesquels le degré max des équations correspondes au nombre le ligne des matrices.

Dans notre exemple, le système d'équation quadrique sera composé de 8 équations de 6e degré.

## Une vérification intermédiaire rapide
Une première vérification consiste à vérifier que les matrices représentant le circuit résolvent le vecteur témoin. L'application est un produit d'Hadamard entre les matrice L, R et O et le vecteur comme illustré ci-dessous. Les valeurs du vecteur sont répliqués sur chaque colonne de la matrice.

Lw . Rw = Ow

```
L.w =
  0  0  1  0  0  0  0  0           1
  0  0  1  0  0  0  0  0         553
  3  0  0  0  0  0  0  0    .      5
  5  0  0  0  0  0  0  0          25
 10  0  0  0  0  0  0  0         125
  3  0  0  0  0  1  1  1         375
                                 125
                                  50

==> L.w
 0 * 1     0 * 553   1 * 5   0 * 25   0 * 125  0 * 375  0 * 125   0 * 50
 0 * 1     0 * 553   1 * 5   0 * 25   0 * 125  0 * 375  0 * 125   0 * 50
 3 * 1  +  0 * 553 + 0 * 5 + 0 * 25 + 0 * 125+ 0 * 375+ 0 * 125 + 0 * 50
 5 * 1     0 * 553   0 * 5   0 * 25   0 * 125  0 * 375  0 * 125   0 * 50
10 * 1     0 * 553   0 * 5   0 * 25   0 * 125  0 * 375  0 * 125   0 * 50
 3 * 1     0 * 553   0 * 5   0 * 25   0 * 125  1 * 375  1 * 125   1 * 50

==> L.w
   5
   5
   3
   5
  10
 553

==> R.w
0 * 1   0 * 553   1 * 5   0 * 25   0 * 125   0 * 375   0 * 125   0 * 50
0 * 1   0 * 553   0 * 5   1 * 25   0 * 125   0 * 375   0 * 125   0 * 50
0 * 1 + 0 * 553 + 0 * 5 + 0 * 25 + 1 * 125 + 0 * 375 + 0 * 125 + 0 * 50
0 * 1   0 * 553   0 * 5   1 * 25   0 * 125   0 * 375   0 * 125   0 * 50
0 * 1   0 * 553   1 * 5   0 * 25   0 * 125   0 * 375   0 * 125   0 * 50
1 * 1   0 * 553   0 * 5   0 * 25   0 * 125   0 * 375   0 * 125   0 * 50

==> R.w
  5
 25
125
 25
  5
  1

==> O.w
0 * 1   0 * 553   0 * 5   1 * 25   0 * 125   0 * 375   0 * 125   0 * 50
0 * 1   0 * 553   0 * 5   0 * 25   1 * 125   0 * 375   0 * 125   0 * 50
0 * 1 + 0 * 553 + 0 * 5 + 0 * 25 + 0 * 125 + 1 * 375 + 0 * 125 + 0 * 50
0 * 1   0 * 553   0 * 5   0 * 25   0 * 125   0 * 375   1 * 125   0 * 50
0 * 1   0 * 553   0 * 5   0 * 25   0 * 125   0 * 375   0 * 125   1 * 50
0 * 1   1 * 553   0 * 5   0 * 25   0 * 125   0 * 375   0 * 125   0 * 50

==> O.w
 25
125
375
125
 50
553
```

On peut facilement vérifier que Lw x Rw = Ow.

# Le twist des équations quadratiques
Cette dernière multiplication fonctionne, mais il est simple de comprendre que si on connait les valeur de la matrice et le vecteur solution on peut remonter au circuit initial. Le premier vrai masqage va consister a faire la même multiplication mais dans le monde des Polynomes en "noyant" les coefficients des matrices dans une série d'équations quadratiques.

Si on prend la première série de coefficient de la matrice L, on a les valeurs : `(0, 0, 3, 5, 10, 3)`, ce sont les coefficients d'entrée aux portes du circuit. Si ces coefficients sont vus comme des coordonnées de l'espace plan : `[(1,0), (2,0), (3, 3), (4, 5), (5, 10), (6, 3)]`. On sait qu'il existe une seule courbe de dimension 5 qui passe par ces 5 points. Elle a la forme `f(x) = a5x^5+a4x^4+a3x^3+a2x^2+a1x+a0`, et que grâce à Lagrange on peut lui faire calculer les coefficient pour passer par les points. On passe alors dans l'espace du signal, et l'ensemble des fonctions de tous les coefficient de passage des portes forme un système d'équation. Ce système d'équation est résolu par une convolution avec le vecteur témoin.

Pour obtenir le système d'équation, il faut transposer les matrices, puis prendre chaque ligne de chaque matrice pour en fabriquer les polynomes de lagrange correspondant.

Le code suivant permet d'obtenir les coefficients des polynômes de Lagrange.

```python
import numpy as np
from scipy.interpolate import lagrange
x = np.array([1, 2, 3, 4, 5, 6])
y = np.array([0, 0, 3, 5, 10, 3])
print(lagrange(x, 1))
```

```
U : Transposé et coordonnées           --> Polynôme (on n'indique que les polynômes différents de 0)

(1,0) (2,0) (3,3) (4,5) (5,10) (6,3)   --> f(x) = -0.225x^5 +3.708x^4 -23.12x^3 +67.79x^2 -90.15x +42
(1,0) (2,0) (3,0) (4,0)  (5,0) (6,0)   --> 0
(1,1) (2,1) (3,0) (4,0)  (5,0) (6,0)   --> f(x) = 0.03333x^5 -0.625x^4 +4.417x^3 -14.38x^2 +20.55x -9
(1,0) (2,0) (3,0) (4,0)  (5,0) (6,0)   --> 0
(1,0) (2,0) (3,0) (4,0)  (5,0) (6,0)   --> 0
(1,0) (2,0) (3,0) (4,0)  (5,0) (6,1)   --> f(x) = 0.008333x^5 -0.125x^4 +0.7083x^3 -1.875x^2 + 2.283x -1
(1,0) (2,0) (3,0) (4,0)  (5,0) (6,1)   --> f(x) = idem U[5]
(1,0) (2,0) (3,0) (4,0)  (5,0) (6,1)   --> f(x) = idem U[5]

V : Transposé et coordonnées           --> Polynôme (on n'indique que les polynômes différents de 0)
(1,0) (2,0) (3,0) (4,0) (5,0) (6,1)    --> f(x) = idem U[5]
(1,0) (2,0) (3,0) (4,0) (5,0) (6,0)    --> 0
(1,1) (2,0) (3,0) (4,0) (5,1) (6,0)    --> f(x) = -0.05x^5 +0.8333x^4 -5.25x^3 +15.67x^2 -22.2x +12
(1,0) (2,1) (3,0) (4,1) (5,0) (6,0)    --> f(x) = 0.125x^5 -2.208x^4 +14.62x^3 -44.79x^2 +62.25x -30
(1,0) (2,0) (3,1) (4,0) (5,0) (6,0)    --> f(x) = -0.08333x^5 +1.5x^4 -10.08x^3 +31x^2 -42.33x +20
(1,0) (2,0) (3,0) (4,0) (5,0) (6,0)    --> 0
(1,0) (2,0) (3,0) (4,0) (5,0) (6,0)    --> 0
(1,0) (2,0) (3,0) (4,0) (5,0) (6,0)    --> 0

W : Transposé et coordonnées           --> Polynôme (on n'indique que les polynômes différents de 0)
(1,0) (2,0) (3,0) (4,0) (5,0) (6,0)   --> 0
(1,0) (2,0) (3,0) (4,0) (5,0) (6,1)   --> f(x) = idem U[5]
(1,0) (2,0) (3,0) (4,0) (5,0) (6,0)   --> 0
(1,0) (2,0) (3,0) (4,0) (5,0) (6,0)   --> f(x) = -0.008333x^5+0.1667x^4-1.292x^3+4.833x^2-8.7x+6
(1,0) (2,1) (3,0) (4,0) (5,0) (6,0)   --> f(x) = 0.04167x^5-0.7917x^4+5.708x^3-19.21x^2+29.25x-15
(1,0) (2,0) (3,1) (4,0) (5,0) (6,0)   --> f(x) = idem à V[4]
(1,0) (2,0) (3,0) (4,1) (5,0) (6,0)   --> f(x) = 0.08333x^5-1.417x^4+8.917x^3-25.58x^2+33x-15
(1,0) (2,0) (3,0) (4,0) (5,1) (6,0)   --> f(x) = -0.04167x^5+0.6667x^4-3.958x^3+10.83x2-13.5x+6
```

Nous obtenons 3 matrices de coefficients de Lagrange. Le nombre de fonctions, représenté par les lignes représentent le nombre de paramètres utilisés dans le circuit, le degré des polynomes correspond au nombre d'opérations du circuit (un degré 5, véhicule 6 opérations).

Nous récrivons ces polynomes sous la forme de matrices (de coefficients) que nous pouvons multiplier avec le vecteur solution, afin de vérifier la même preuve que précédemment mais dans l'espace des polynômes.
Uw . Vw = Ww

`w = [ 1 553 5 25 125 375 125 50]`
```
U:
[
 [ -0.225, 0,  0.033, 0, 0,  0.008,  0.008,  0.008]
 [  3.708, 0, -0.625, 0, 0, -0.125, -0.125, -0.125]
 [-23.125, 0,  4.417, 0, 0,  0.708,  0.708,  0.708]
 [ 67.792, 0,-14.375, 0, 0, -1.875, -1.875, -1.875]
 [-90.15 , 0, 20.55 , 0, 0,  2.283,  2.283,  2.283]
 [ 42    , 0, -9.   , 0, 0, -1    , -1    , -1   ]
]
Uw = 4.525x^5-68.17x^4+388.5x^3-1035x^2+1268x-553
```

```
V:
[
 [ 0.008, 0,  -0.05 ,   0.125,  -0.083, 0, 0, 0]
 [-0.125, 0,   0.833,  -2.208,   1.5  , 0, 0, 0]
 [ 0.708, 0,  -5.25 ,  14.625, -10.083, 0, 0, 0]
 [-1.875, 0,  15.667, -44.792,  31    , 0, 0, 0]
 [ 2.283, 0, -22.2  ,  62.25 , -42.333, 0, 0, 0]
 [-1    , 0,  12    , -30    ,  20    , 0, 0, 0]
]
Vw = -7.492x^5+136.3x^4-920.3x^3+2832x^2-3844x+1809
```

```
W:
[
 [0,  0.008, 0, -0.008,   0.042,  -0.083,   0.083, -0.042]
 [0, -0.125, 0,  0.167,  -0.792,   1.5  ,  -1.417,  0.667]
 [0,  0.708, 0, -1.292,   5.708, -10.083,   8.917, -3.958]
 [0, -1.875, 0,  4.833, -19.208,  31    , -25.583, 10.833]
 [0,  2.283, 0, -8.7  ,  29.25 , -42.333,  33    , 13.5  ]
 [0, -1    , 0,  6    , -15    ,  20    , -15    ,  6    ]
]
Ww = -13.31x^5+254.8x^4-1792x^3+5652x^2-7724x+3647
```

*Attention les polynômes Uw, Vw, Ww indiqués ici sont arrondis par les affichages. Les erreurs d'arrondis peuvent faire dévier fortement les courbes...*

La multiplication de la matrice de lagrange par le vecteur témoin se fait par le code python suivant :
```python
import numpy as np
from numpy import poly1d

V = np.array(
[[  0.008, 0,  -0.05 ,   0.125,  -0.083, 0, 0, 0],
 [ -0.125, 0,   0.833,  -2.208,   1.5  , 0, 0, 0],
 [  0.708, 0,  -5.25 ,  14.625, -10.083, 0, 0, 0],
 [ -1.875, 0,  15.667, -44.792,  31    , 0, 0, 0],
 [  2.283, 0, -22.2  ,  62.25 , -42.333, 0, 0, 0],
 [ -1,     0,  12    , -30    ,  20    , 0, 0, 0]])

witness = [1, 553, 5, 25, 125, 375, 125, 50]

Vw = np.matmul(V, witness)
print(poly1d(Vw))
```
# L'application de la preuve
Si l'isomorphisme fonctionne, nous pouvons faire l'opération de controle. Dans le monde R1CS nous avons vérifié que `Lw . Rw = Ow`. Nous devrions avoir par similitude dans le domaine des Polynômes : `Uw * Vw = Ww`.  

On peut constater un problème sur les degrés des polynômes. La multiplication des Polynômes Uw par Vw va nécessairement aboutir sur un polynôme de degré 10. Il faut donc annuler les degrés supérieurs au degré de Ww. Cela se fait par une polynome de degré deg(Uw * Vw) - deg(Ww).  
`H(t) = (x-1)(x-2)(x-3)...(x-10)` 

`Uw * Vw = Ww + H`
Le polynome H n'a aucune chance d'annuler le l'innégalité, car il est choisi de manière arbitrairement connu.  
`(Uw * Vw) - Ww != H`  

L'idée est de décomposer le polynôme H, en réduisant sa dimension pour avoir 2 termes dont un est connu h, l'autre ne fait qu'annuler l'équation.
`(Uw * Vw) - Ww = h * t`  

`h * t` doit être de la dimension de `(Uw * Vw)`, t peut être fabriqué commme voulu. On peut donc écrire l'équation suivante :
`((Uw * Vw) - Ww) / t = h`

Si t est un diviseur parfait de `((Uw * Vw) - Ww)` alors votre équation Qap fonctionne et vous avez fourni la preuve que vous connaissez le polynome initialement utilisé `f(x)=3x^3+5x^2+10x+3`.

En effet la probabilité de connaître un polynôme unique qui relie les signaux U, V, et W par un diviseur cible t est nulle. Vous pouvez donc vérifier cette proposition en vérifiant que le reste de la division est nulle.

Dans notre exemple, le code python suivant, indique un reste proche de 0 qu'on peut considérer nul.
```python
import numpy as np
from numpy import poly1d

Uw = poly1d([4.525,-68.16666667,388.54166667,-1035.33333333,1268.43333333,-553])
Vw = poly1d([-7.53333333,136.33333333,-920.33333333,2831.66666667,-3844.13333333,1809])
Ww = poly1d([-13.30833333,254.83333333,-1791.625,5651.66666667,-7723.56666667,3647])

t = poly1d([1, -1])*poly1d([1, -2])*poly1d([1, -3])*poly1d([1, -4])*poly1d([1, -5])*poly1d([1, -6])

(h, reste) = ((Uw * Vw)-Ww)/t

print("h \n", h)
print("reste \n", reste)
```
`    h : -34.09x^4+414.6x^3-1713x^2+2734x-1394`
`reste : 0.0001015x^5-0.001524x^4+0.00865x^3-0.02295x^2+0.028x-0.01228`

A titre de comparaison la fonction résultante ((Uw*Vw)-Ww) est la suivante  
`-34.09x^10+1130x^9-1.638e+04x^8+1.363e+05x^7-7.187e+05x^6+2.5e+06 x^5-5.792e+06 x^4+8.785e+06x^3-8.321e+06x^2+4.428e+06x-1.004e+06`

Le tracé de la fonction résultante et du reste permet de visualiser concrêtement le caractère hortogonal de ces fonctions.
(visual)


Le soucis majeur du système dans l'état où il se trouve est qu'il n'est pas succinct. Si on réalise un circuit complexe le système d'équation va devenir rapidement incalculable pour le prouveur et le vérifieur.

l'étape suivante va consister à porter ce principe dans un espace plus efficace à calculer. A savoir passer sur de l'arithmétique modulaire et projet les données dans l'espace des courbes elliptiques.

# Simplifier les équations


Ils sont utilisés pour prouver qu'une information est vraie sans révéler l'information elle-même. Les zk-SNARKs sont utilisés dans de nombreuses blockchains, notamment Zcash, Ethereum et Tezos.

#### Fonctionnement technique :

###### Traduction d'un probleme en un circuit arithmetique :

Ce polynome x^3+x+5 donnerai en circuit arithmetique :

1. sym_1=x*x
2. y=sym_1*x
3. sym_2=y+5
4. out=sym_2

###### Convertion circuit en R1CS :

On va prendre trois vecteur A,B et C
Puis pour chaque porte du circuit on va avoir une contrainte de la forme :
A[i]*B[i]=C[i]
Ainsi pour notre circuit on aura :
Pour la première porte :

1. A[1]=x
2. B[1]=x
3. C[1]=sym_1

...

A la fin de cette étape on doit avoir 3 matrice A B C de taille n*m avec n le nombre de porte et m le nombre de variable.
et un vecteur S de taille m qui contient les valeurs des variables. ex : S =  [1,x,out,sym_1,y,sym_2]

###### Convertion R1CS en QAP :

On va trouver des polynomes. Chaque matrice A B C va donner m polynome.
Pour les trouver on va utiliser le lemme de lagrange.
On va prendre A[1]t=[0,1,0,5] par exemple
et en doit trouver un polynome qui passe par (1,0) (2,1) (3,0) (4,5)
grâce au lemme de lagrange on peut trouver un polynome qui passe par ces points.

Donc maintenant A B C donnent les coeff des polynomes.

On va utliser A B C pour trouver les polynomes H L R qui sont les polynomes qui vont nous permettre de verifier la preuve.

A suivre...

##### Pour la suite:

On sait un peu près comment formaliser ses preuves, ensuite il va falloir penser qu'on travail dans des groupes fini Z/nZ et le point important est l'utilisation des courbes elliptiques ??









---

### Groth16

Article medium qui explique le fonctionnement : [Under the hood of zkSNARK Groth16 protocol (part 1) | by Crypto Fairy | Coinmonks | Sep, 2023 | Medium](https://medium.com/coinmonks/under-the-hood-of-zksnark-groth16-protocol-2843b0d1558b)

Code python : [zkSNARK-under-the-hood/groth16.ipynb at main · tarassh/zkSNARK-under-the-hood · GitHub](https://github.com/tarassh/zkSNARK-under-the-hood/blob/main/groth16.ipynb)

article de ref de groth16 : [260.pdf (iacr.org)](https://eprint.iacr.org/2016/260.pdf)





Groth16 est spécifiquement un protocole de preuve pour les preuves succinctes non interactives d'argument de connaissance (zk-SNARKs). Il est particulièrement connu pour être très efficace en termes de taille de preuve et de temps de vérification. Dans un zk-SNARK, le prouveur peut générer une preuve que certains éléments d'entrée satisfont une certaine relation sans révéler les éléments eux-mêmes. Cette preuve peut être vérifiée très rapidement, même si la relation est complexe.

Le zk-SNARK Groth16 est largement utilisé car il permet de créer des preuves très petites qui peuvent être vérifiées en un temps constant, indépendamment de la complexité de l'affirmation. C'est essentiel pour les applications blockchain où la bande passante et le temps de calcul sont des ressources précieuses.



##### Partie 1:

"Here is an image that depicts the zkSNARK setup. Unlike other ZKP protocols such as STARK and Bulletproofs, zkSNARK requires a third party during the initialization phase. This third party provides the prover and verifier with their respective keys."

"the execution time will tend to be greater on the prover’s side."

"in the case of SNARKs, computations must be bounded. This means the number of iterations must be known in advance, and the number of parameters, as well as their size, should also be predetermined."



"There are several libraries capable of performing this conversion, including:

- [Zokrates](https://github.com/Zokrates/ZoKrates): The code is written in a language resembling Python.
- [Circom](https://github.com/iden3/circom): It uses its own domain-specific language.
- [Pequin](https://github.com/pepper-project/pequin) from the Pepper-Project: This utilizes a C-like language, similar to the gist provided above."



Pour construit le circuit il faudrait factoriser au max pour avoir le moins de constraint possible à la fin "The primary objective here is to identify the fewest constraints that can accurately represent this equation."

<img src="https://miro.medium.com/v2/resize:fit:875/1*x3BJS5DA5i1sJ6MpHjicgA.png" title="" alt="" data-align="center">



#### Partie 2 :

"in *GF(p)*:

*p = 21888242871839275222246405745257275088548364400416034343698204186575808495617*

The value *p* is a prime number, so the set under consideration comprises integers ranging from 0 to *p*−1. This specific choice is pivotal because of the Elliptic Curve known as *BN-128*, which we will later employ for encryption. Notably, within the Ethereum blockchain’s framework, *BN-128* and *secp256k1* are the only supported elliptic curves."



witness vector:

<img src="https://miro.medium.com/v2/resize:fit:805/1*6yzb6iqFaT2SoFaJV1BGLQ.png" title="" alt="" data-align="center">



Finally, if we multiply each matrix by witness vector we will get next:

<img src="https://miro.medium.com/v2/resize:fit:393/1*PqHEXvk3CPjalnwvpWCOXw.png" title="" alt="" data-align="center">

Where *Lw*, *Rw*, and *Ow* are vectors. The element-wise multiplication of *Lw* and *Rw* should yield *Ow*. If this equality holds true, it confirms the correctness of our R1CS defined by the matrices *L*, *R*,*O* and vector *w*.

#### Partie 3 :

However, in the first article, I emphasized the importance in zkSNARK of maintaining a verifier time that is either constant or close to it — represented as O(1). Evaluating *Lw*×*Rw*=*Ow* by verifiers isn’t inherently O(1) as it’s contingent on the program’s size. Furthermore, introducing encryption into the mix further decelerates execution. Therefore, we need a more concise representation than R1CS, and this is where QAP comes into play

Homomorphism: Let’s simplify this concept. In Abstract Algebra, we study numbers, categorize them, and then organize them into groups based on specific rules — this is known as Group Theory. Within Group Theory, we also explore the relationships between these groups. At its core, a homomorphism is a mapping between two groups that preserves their inherent structures. Think of it as a bridge that allows us to relate operations in one group to another. Interestingly, the vector space where R1CS resides and the space of polynomials can be thought of as two such groups, and there exists a homomorphism between them. For those diving deeper, it’s worth noting that both vectors and polynomials technically belong to the category of “Rings”. I’ll provide a link at the end of this article for those curious to learn more.

## QAP

So our new goal is to move from vector field to polynomial field:

<img src="https://miro.medium.com/v2/resize:fit:683/1*VGm1yoiXQC-S_jhERXAW9Q.png" title="" alt="" data-align="center">



Dans cette partie on a trouver les matrices de polynome pour L R O

Ensuite on a calculer U=Lw, V=Rw, W=Ow dans le corps de Galois toujours

Et maintenant si on teste avoir un x aléatoire pour voir sur le reste est nul



<img src="https://miro.medium.com/v2/resize:fit:578/1*-fdN6ag6L6cnmrtahGlpgA.png" title="" alt="" data-align="center">



#### Partie 4 :

The Groth16 protocol, for instance, employs a specific elliptic curve known as BN254.

we need to place Bob and Alice within a common “framework” or “environment.” This is where Elliptic Curves come into play.

Here are a few introductory remarks about Elliptic Curves (ECs):

1. ECs belong to the category of Finite Field Groups from Abstract Algebra.
2. When you select a point on an Elliptic Curve and “multiply” it by a number, you’ll derive another point on that same curve. However, reverse-engineering the original number from the resulting point is a formidable challenge. This mechanism is reminiscent of a coding or encryption process.
3. Adding two points on the curve will yield a new point.
4. Not all Elliptic Curves can be employed for this purpose. The curve must be “pairing-friendly.” While this might sound abstract, it essentially means that when you pair a point from one group with a point from another group, the outcome will belong to a third distinct group.

<img src="https://miro.medium.com/v2/resize:fit:368/1*FRPntmukUp7bgtulgVN3Og.png" title="" alt="" data-align="center">

First, we require an intermediary — the “trusted setup.” This entity will place Alice and Bob within a unified environment. The trusted setup provides them with essential parameters, but in an encrypted format, ensuring that neither Alice nor Bob can decipher their true nature. This is crucial, as we don’t want to leave it to chance or rely on the assumption that Alice or Bob will act with integrity.

We now have our initial prover program. To reemphasize, this setup is not yet secure. Since Alice merely presents three points on the elliptic curve, there’s nothing to confirm that any actual computation took place. In the subsequent article, we’ll introduce additional parameters to transform this into a genuine proof.

#### Partie 5 :

So far, we’ve managed to compress the prover’s work evaluation into three points on elliptic curve: A, B, and C. Here’s a brief recap of how it looked in the beginning:

- The R1CS was represented as a matrix multiplication *Lw*​×*Rw*​=*Cw*​.
- Then, thanks to homomorphism, the R1CS was transformed into the QAP in polynomial form, given by *U*(*τ*)×*V*(*τ*)=*W*(*τ*)+*H*×*T*(*τ*).
- Now, it’s represented in the form of elliptic curve points: *A*×*B*=*C*

![](https://miro.medium.com/v2/resize:fit:833/1*NbI9W51BYXY2VPO1TBl61A.png)

*A*×*B*=*C*



# α, β

Although the structure is preserved, we must introduce constraints to this equation to fully realize it as a zkSNARK. When the verifier receives points *A, B*, and *C*, they cannot determine if these points are genuine results of an evaluation or merely a trick by the prover. For this very reason, we need to introduce two additional parameters, *α* (alpha) and *β* (beta). These parameters must be provided by a trusted setup agent:

![](https://miro.medium.com/v2/resize:fit:650/1*unZ_bnl1enOtWwD9z_u20A.png)

Now, the prover must compute *(A + α), (B + β), βA, αB*, and *C*. Meanwhile, the verifier will have to compute the *αβ* pairing aka “multiplication” (values provided by the trusted setup) and check if the equation is valid

We must revisit the matrices *Lp*​, *Rp*​, and *Op*​, which contain the polynomial coefficients. It’s necessary to compute *β*×*Lp*​ and *α*×*Rp*​. Eventually, these calculations will yield the values *βA* and *αB.* Setup agent is responsible for calculating these parameters.

As for verifier, unfortunately, python library doesn’t support additions for pairings but if it would it may look like this:

```python
# A = A + α
# B = B + β
# C = βA + αB + C
# AB == αβ + [βA + αB + C]
assert pairing(B_G2, A_G1) == pairing(beta_G1, alpha_G1) + pairing(G2, C_G1)
```

Fortunately we can do it in solidity but we have to move A*B to the right side:

![](https://miro.medium.com/v2/resize:fit:375/1*P9cqqRpz4pbH-HKt7r52sw.png)

***Note****:* Ideally, points A, B, and C should be provided as input parameters to the `verify` function. However, for the sake of simplicity in this demonstration, they have been hardcoded. To witness this in action, you can import this contract into Remix Studio, compile it, and deploy it. You'll observe that the result returns `true`



![](https://miro.medium.com/v2/resize:fit:643/1*srZCBdRIK0jt7zRqXC1Gtw.png)

Until now, this data was treated as private. However, in this example, I aim to designate both ‘1’ and ‘out’ as public parameters. To achieve this, we must split the vector into two pieces.

![](https://miro.medium.com/v2/resize:fit:543/1*k_1zLzREVWQEmuDFR83xxw.png)

**Note**: The sequence should remain as **[1, out]** followed by [x, y, …, v4]. If there’s a requirement to reveal other data (e.g., *y* and *v*4), you must rearrange these entries so they can be split into two sections. This means that the matrices *L*, *R*, and *O* for the arithmetic circuit will also need adjustments.



We split the pre-image of point C, represented as *βU*+*αV*+*W*+*HT*, into two parts:

1. *c* = [*βU*+*αV*+*W*+*HT*] — This is the polynomial for the private input.
2. *k* = [*βU*+*αV*+*W*] — This is the polynomial for the public input.

For the pre-images of A and B, represented as *U*+*α* and *V*+*β* respectively, nothing has changed. Final equation will look like this:

![](https://miro.medium.com/v2/resize:fit:358/1*AX6aaaScgwXFvJB_8we5rQ.png)

The prover will supply *A*′, *B*′, and *C*. The values of *α* and *β* are provided to the verifier from the trusted setup. The verifier is responsible for calculating the point *K*. The prover is required to present the values [1 out] in an unencrypted form. To encrypt these values, the verifier will employ elliptic curve scalar multiplication, and the necessary points for this operation will be supplied by the setup ([k1] * 1 + [k2] * out).



To reiterate: In an ideal scenario, the smart contract should accept points *A*, *B*, *C*, and the ‘public input’ as function arguments. However, for the sake of simplicity in this demonstration, all values have been hard-coded. These can be easily verified in Remix Studio or [here](https://mumbai.polygonscan.com/address/0xe529a6ba0847a2e7e2335fbb29ea2eaa3ee00b85#readContract).





#### Partie 6:

a relire



#### Conclusion:

Les 6 papiers sont très bien expliqués avec du bon code python qui fonctionnent très bien !

Il faudra voir sur le code solidity fonctionne bien. Pour quoi pas faire 3 programmes pour le setup/prover/verifier pour savoir exactement ce qu'ils ont en commun comme data.

Il va pas assez loin des les explications, on peut mieux faire. Il faut que je lisse + de papier sur EC:

- https://medium.com/blockapex/a-primer-for-the-zero-knowledge-cryptography-part-ii-ecc0199d0a56

- https://medium.com/@imolfar/why-and-how-zk-snark-works-8-zero-knowledge-computation-f120339c2c55

Il a aussi fait un article il y a quelques jours sur PLONK : [Under the hood of zkSNARKs — PLONK protocol: Part 1 | by Crypto Fairy | Nov, 2023 | Medium](https://medium.com/@cryptofairy/under-the-hood-of-zksnarks-plonk-protocol-part-1-34bc406d8303)































##### Ressources :

###### Point de départ vers beaucoup de ressource :

https://github.com/matter-labs/awesome-zero-knowledge-proofs

###### 3 videos que modelise un problème en circuit arithmetique et le converti en R1CS et QAP et ECC:

https://www.youtube.com/watch?v=tR4r4dxL66k
https://www.youtube.com/watch?v=T2wlGhVFOCw
https://www.youtube.com/watch?v=bqSFyULJFtQ

###### Les 3 articles de Vitalik Buterin sur les zk-SNARKs :

https://medium.com/@VitalikButerin/quadratic-arithmetic-programs-from-zero-to-hero-f6d558cea649
  Plus d'explication sur l'article de Vitalik:
   https://risencrypto.github.io/R1CSQAP/
   https://webcache.googleusercontent.com/search?q=cache:https://medium.com/asecuritysite-when-bob-met-alice/filling-in-the-details-of-vitalics-excellent-zk-snarks-article-for-qap-processing-8b36fcf69f46
Vitalik recommende de lire ça : https://chriseth.github.io/notes/articles/zksnarks/zksnarks.pdf

https://medium.com/@VitalikButerin/exploring-elliptic-curve-pairings-c73c1864e627
https://medium.com/@VitalikButerin/zk-snarks-under-the-hood-b33151a013f6

###### Un article sur les elliptic curves :

https://blog.cloudflare.com/a-relatively-easy-to-understand-primer-on-elliptic-curve-cryptography/

###### Eli Ben-Sasson sur les zk-SNARKs :

https://eprint.iacr.org/2013/879.pdf
https://www.youtube.com/watch?v=HJ9K_o-RRSY

###### Utilisation de libsnark pour les zk-SNARKs :

https://github.com/christianlundkvist/libsnark-tutorial

##### Rareskills.io
Site de vulgarisation des maths pour les programmeur crypto
- Théorie des ensembles : https://www.rareskills.io/post/set-theory
  - Termes définis : ensemble / magma / semi-groupe / monoid / groupe
      - Semigroup : pas d'élément identite (0 dans l'addition)
      - Monoid : identité, mais pas d'inverse (-1 / +1)
      - Groupe : identité + inverse
- Théorie des groupes : https://www.rareskills.io/post/group-theory-and-coding
  - groupe : ensemble muni de
            - Un opérateur binaire associatif et fermé
            - Un élément identité
            - Les éléments possèdent un inverse
      - Groupe Abélien : groupe muni de
            - L'opérateur binaire associatif et fermé est aussi commutatif (ex : +)
  - groupe fini
  - ordre d'un groupe
  - groupe cyclique : tous les éléments sont générés par un générateur additionné pleins de fois
- Anneau et Champs : https://www.rareskills.io/post/rings-and-fields
  - Anneau : ensemble muni de deux opérateurs binaires
    - Sous le premier opérateur, l'ensemble est un groupe abélien(inverse et commutatif)
    - Sous le second, l'ensemble est un monoid(pas d'inverse)
    - Le second opérateur distribue sur le premier
  - Champ : pareil qu'un anneau
    - Premier opérateur pareil que l'anneau
    - Second opérateur si on exclue le 0, l'ensemble est un groupe abélien

    Exemple : Addition et multiplication modulo 2 est le plus petit champ possible (cf GF(2))
    Exemple : l'ensemble des entiers avec + et * n'est pas un champ, mais un anneau
    Exemple : l'ensemble de réels est un champ

- Courbe elliptiques sur les champs finis : https://www.rareskills.io/post/elliptic-curves-finite-fields
  - Très bon article sur le principe de y^2 = X^3 + 3 (mod 27)
    - Base des zkp : x + y = 5, je peux prouver que je connais deux chiffres x et y solution, sans les donner.
    -      Je peux donner : GX, et GY.
    -        Grace aux courbes elliptiques le vérifieur peut faire
    -                GX + GY = 5G
    - ==> On suppose qu'un attaquant qui connait GX, ne peux pas revenir à X. C'est le principe des algorithmes discrets
    - ==> Si un attaqueur imagine x et y, il peut par contre vérifier que ce sont les bonnes valeur sur les points de la courbe elliptique

- Billinear Pairing : Pour l'instant pas compris : https://www.rareskills.io/post/bilinear-pairing
Le principe est de permettre la multiplication de deux coordonnées de courbes elliptiques. Dans la même courbe (G1) cela correspond à un produit scalaire, qui est l'addition du point sur lui-même autant de fois que possible.
kA = A + A + A. et A + B = C sont des points d'une même courbe. Le pairing permet de faire une multiplication de points de deux courbes différentes pour se retrouver sur une troisième courbe.
A x B = C, le principe est que les points sont sur trois courbes différentes qui ont des propriétés de champs étendus similaire (à vérifier). Le pairing est une fonction qui rend homomorphe la multiplication sur des courbes elliptique.
5G2 * 6G1 = 30 G12. D'une manière générale elle est utilisée pour comparer des pairing. Les points de la courbe G23 ne sont pas forcément accessibles (volume mémoire). On veut vérifier des équalités du style :
Pairing(G2 * 5, G1 * 6) = Pairing (30*G2, G1). Tout se fait dans G12, mais c'est invisible.



- R1CS to Quadratic Arithmetic Program over a Finite Field in Python : https://www.rareskills.io/post/r1cs-to-qap
- Converting Algebraic Circuits to R1CS (Rank One Constraint System) : https://www.rareskills.io/post/rank-1-constraint-system

- Circom : code rust pour écrire des circuits R1CS (version précédente en js) : https://docs.circom.io/


# Preuves à Divulgation Nulle de Connaissance (ZKP)
Les ZKP visent à prouver une assertion sans divulguer de valeurs et sans connaître les détails de l'assertion. Le principe est directement issu des casses-têtes. Je peux montrer que je connais la solution sans divulguer les étapes intermédiares. Dans l'exercice du Sudoku, je peux montrer que j'ai trouvé 10 chiffres différents sur toutes les lignes et toutes les colonnes. Le ZKP modélisent ce principe. La mécanique générale met en relation un **prouveur** qui indique connaître la solution au problème et un **vérifieur** qui contrôle que la solution proposée. Cet échange se fait dans un cadre contraint contrôlé par un tier de confiance que nous appelons le **confident**. Par exemple dans le cadre concrêt du Sodoku, le **confident** peut être vu comme  celui qui prépare la grille initiale et qui vérifie que le prouveur n'a pas trouvé une solution toute prête ailleurs. 
  
## Principes généraux des zksnarks et groth16
Nous présentons le détail du fonctionnement mathématique de l'approche ZkSnark mise en œeuvre dans l'implantation groth16. Les Zksnarks est une famille de preuves ZKP qui possèdent des propriétés communes. Elles sont **Succinctes** et **Non interactives**. **Succincte** indique que le vérifieur peut contrôler la solution rapidement. **Non interactive** indique que le **prouveur** n'envoie qu'un seul message contenant la solution au **vérifieur**. En effet dans l'exemple du Sudoku, en supposant que les lignes et les colonnes sont données une par une, la preuve se fait de manière interactive. A chaque ligne ou colonne présentée au **vérifieur** sa confiance dans la preuve augmente. 

Partons du polynôme : $f(x) = 3x^3+5x^2+10x+3$ et un `x` sur la courbe que seul le **prouveur** connait. Le **prouveur** veut montrer au vérifieur qu'il a bien exécuté cette fonction sur une valeur de `x`qu'il a choisi. Le **prouveur** doit pouvoir valider cette assertion sans avoir de doute et rapidement. 

La question est la suivante, en tant que **prouveur** "Comment prouver à une personne que je connais ce polynôme ? " sans lui indiquer les coefficients (3, 5, 10, 3) ni les degrés correspondants.

<p align="center">
  <img src="./img/plotPoint-fx.png" width="200">
</p>

Si je trace la courbe, je peux présenter au **vérifieur** des paires de valeurs telles que (0, 3), (1, 21), (2, 67) et (3, 159), il peut en déduire que je suis au courant de l'existence d'une courbe spécifique de degré 3, puisqu'une seule courbe de ce type peut relier ces quatre points. Cependant, ce processus comporte un risque : le vérifieur pourrait potentiellement retrouver la courbe originale à partir de ces informations, ce qui compromet l'objectif de cacher la courbe. D'un autre côté, il est aussi possible que j'aie fabriqué ces points sans fondement réel.

Nous sommes face à deux défis : démontrer ma connaissance du polynôme sans divulguer les coefficients spécifiques, et garantir que le masquage ne me permet pas de choisir des valeurs aléatoires.

Pour Zksnarks, le **prouveur** va montrer au vérifieur qu'il a exécuté un polynôme avec une valeur spécifique donnée. La preuve fournie ne permet ni de remonter au polynôme exécuté ni à la valeur d'entrée. La preuve zkSnark, se fait en 5 étapes. 
- Transformation du polynôme dans un circuit R1CS
- Récupération des coefficients du circuit et calcul du vecteur témoin (point solution de l'équation)
- Conversion des coefficients dans un système d'équations quadratique (QAP)
- Application du vecteur témoin au système QAP afin d'obtenir trois courbes ayant pour solution le circuit initial
- Projection des courbes dans un espace elliptique

# La preuve Zksnark
## Transformation de l'équation dans un circuit R1CS
Le Circuit R1CS, ou Rank 1 Constraint System, est une structure utilisée pour transformer des équations polynomiales complexes en une série d'opérations élémentaires modélisées par des porte. Chaque porte effectue une multiplication, avec une entrée gauche, une entrée droite et une sortie. Les portes sont enchaînées afin d'obtenir un circuit équivalent au polynôme initial. 
<p align="center">
  <img src="./img/porteLRO.png" width="200">
</p>

Considérons un exemple concret avec notre polynôme $f(x) = 3x^3 + 5x^2 + 10x + 3$. Sa conversion en circuit R1CS se décompose en portes, où chaque opération polynomiale est transformée en une série de multiplications:
```
v1 = x * x   (1)  
v2 = x * v1  (2)  
v3 = 3 * v2  (3)  
v4 = 5 * v1  (4)  
v5 = 10 * x  (5)  
out = v3 + v4 + v5 + 3 (6)  
out = (v3 + v4 + v5 + 3) * 1 (6bis)  
```
Le schéma suivant présente le circuit équivalent sous forme de portes. La dernière porte regroupe toutes les sorties nécessaires afin de réaliser l'addition terminale du polynôme.  

<p align="center">
  <img src="./img/circuit-fx.png" width="200">
</p>


Dans le circuit R1CS, chaque étape est représentée par une porte logique, intégrant des entrées et une sortie basées sur la multiplication. Pour s'aligner avec les contraintes du circuit, les additions sont traitées en regroupant les signaux en amont des portes. Ainsi, la dernière étape où `out` est calculé devient une multiplication par 1 pour respecter la forme standard du R1CS : $O = L * R$.

Le circuit est ensuite exprimé sous forme de trois matrices distinctes, correspondant aux éléments gauche (L), droite (R) et sortie (O) du circuit. Ces matrices détaillent comment chaque variable et chaque étape intermédiaire sont reliées entre elles dans le circuit. Les colonnes de la matrice représentent les différentes variables utilisées dans le circuit R1CS `[ 1 out x v1 v2 v3 v4 v5 ]`.  Le circuit établi est constitué de 6 portes et 8 variables. La variable `1` représente les constantes du système, `out` représente la valeur de sortie du polynôme, `x`la valeur d'entrée, `v1-vx` les valeurs intérmédiaires des portes du circuit R1CS.

Le système d'équation se résume à 3 matrices exprimant respectivement les entrées gauches (L), les entrées droites (R) et les sorties du circuit. 

```
//L    
//1 out x v1 v2 v3 v4 v5  
[  
  0  0  1  0  0  0  0  0    // 1: x  
  0  0  1  0  0  0  0  0    // 2: x  
  3  0  0  0  0  0  0  0    // 3: 3  
  5  0  0  0  0  0  0  0    // 4: 5  
 10  0  0  0  0  0  0  0    // 5: 10  
  3  0  0  0  0  1  1  1    // 6: (6bis)  
]
```
On retrouve l'état des 8 variables en colonne pour chaque porte en ligne.
La ligne 4 de la matrice L indique qu'à l'entrée gauche de la porte 4 il y a une constante 5.  

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
Ici, La ligne 4 de la matrice L indique qu'à l'entrée droite de la porte 4 il y a la valeur v1.  

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
Ce circuit simule l'exécution du polynôme par étapes successives représentées par des additions et des multiplication d'entiers. 

Pour une valeur donnée de `x`, par exemple `5`, la valeur de sortie du polynôme est $f(5) = 553$. Cette valeur peut également se calculer au travers du système R1CS. On peut stocker les valeurs des variables intermédiaire dans le vecteur suivant : `w = [ 1 553 5 25 125 375 125 50]`. 

Le circuit R1CS fonctionne avec le produit [matriciel d'Hadamard](https://fr.wikipedia.org/wiki/Produit_matriciel_de_Hadamard) `Lw ☉ Rw = Ow`, que l'on peut vérifier avec le code python suivant [code/r1cs.py](code/r1cs.py) et détaillé plus loin.
```python
import numpy as np
import random
# Equation 3x^3 + 5x^2 + 10x + 3
# Définition des matrices R1CS
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

# x aléatoire
x = random.randint(1,1000)

# Circuit initial
v1 = x * x
v2 = x * v1
v3 = 3 * v2
v4 = 5 * v1
v5 = 10 * x
out = v3 + v4 + v5 + 3

w = np.array([1, out, x, v1, v2, v3, v4, v5])

result = O.dot(w) == np.multiply(L.dot(w),R.dot(w))
assert result.all(), "Le produit ne fonctionne pas"
print("--> Vecteur choisi", w)
```

Le produit matriciel d'Hadamard, ce décompose ainsi.
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

On peut facilement vérifier que `Lw ☉ Rw = Ow`.

# Les équations quadratiques
## Transposition initiale
Ces matrices (LRO) ne font que représenter le polynôme initial en le décomposant en coefficients de matrices.  
L'étape suivante de zkSnark consiste à transformer masquer la valeur de ces coefficients dans des courbe. La courbe passe en 0 par les points correspondants aux coefficients. 

Par exemple, si on prend la première série de coefficient de la matrice L, on a les valeurs : `(0, 0, 3, 5, 10, 3)`, ce sont les coefficients d'entrée gauche des portes du circuit. On peut modéliser ces entrée par une courbe qui donne les mêmes coefficients. Ainsi le vecteur $[0, 0, 3, 5, 10, 3]$ peut être modélisé par une courbe qui passe par les points  $[(1,0), (2,0), (3, 3), (4, 5), (5, 10), (6, 3)]$.

On sait qu'il existe une seule courbe de dimension 6 qui passe par ces 6 points. Elle a la forme $f(x) = a5x^5+a4x^4+a3x^3+a2x^2+a1x+a0$. L'interpolation de Lagrange permet de calculer la courbe qui passe par ces points [code/lagrange.py](code/lagrange.py). Il faut bien noter que les matrices U, V, W sont des transposées par rapport à R,L,O. Elle contiennent 8 lignes correspondant aux courbes de chaque paramètre du vecteur témoin et les fonctions interpolées sont de degré 5 correspondant aux 6 portes traversées. 

```python
import numpy as np
from scipy.interpolate import lagrange
x = np.array([1, 2, 3, 4, 5, 6])
y = np.array([0, 0, 3, 5, 10, 3])
print(lagrange(x, y))
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

Nous obtenons 3 matrices de coefficients de Lagrange. Dans notre exemple 8 variables de circuit pour 6 opérations.

Nous récrivons ces polynomes sous la forme de matrices (de coefficients) que nous pouvons multiplier avec le vecteur solution, afin de vérifier la même preuve que précédemment mais dans l'espace des polynômes.
`Uw . Vw = Ww` est valide aux points d'interpolation (1, 2, 3, 4, 5, 6).

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
```

<p align="center">
  <img src="./img/U.png" width="200">
</p>
$Uw(x) = 4.525 x - 68.17 x + 388.5 x - 1035 x + 1268 x - 553$


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
```
<p align="center">
  <img src="./img/V.png" width="200">
</p>
$Vw(x) = -7.533 x + 136.3 x - 920.3 x + 2832 x - 3844 x + 1809$


```
W:
[
 [0,  0.008, 0, -0.008,   0.042,  -0.083,   0.083, -0.042]
 [0, -0.125, 0,  0.167,  -0.792,   1.5  ,  -1.417,  0.667]
 [0,  0.708, 0, -1.292,   5.708, -10.083,   8.917, -3.958]
 [0, -1.875, 0,  4.833, -19.208,  31    , -25.583, 10.833]
 [0,  2.283, 0, -8.7  ,  29.25 , -42.333,  33    , -13.5  ]
 [0, -1    , 0,  6    , -15    ,  20    , -15    ,  6    ]
]
```
<p align="center">
  <img src="./img/W.png" width="200">
</p>
$Ww(x) = -13.31x^5+254.8x^4-1792x^3+5652x^2-7724x+3647$

Une multiplication de matrice par le vecteur témoin se fait par le code python suivant [mult](code/mult.py)
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

Pour éviter les erreurs d'arrondis, on peut vérifier que `Uw.Vw = Ww` est valide aux points d'interpolation avec le code suivant. [valideUwVwWw](code/valideUwVwWw.py)

```python
import numpy as np
from numpy import poly1d
from scipy.interpolate import lagrange

errMax = 0.0000001
witness = [1, 553, 5, 25, 125, 375, 125, 50]
x = np.array([1, 2, 3, 4, 5, 6])

def calculPoly(mat):
    Lt = np.transpose(mat)
    res = []
    for i in range(0, len(Lt)):
        y = Lt[i]
        lArray = lagrange(x, y).coeffs
        if (len(lArray) == 1):
            lArray = np.zeros(len(mat))

        res.append(lArray)

    return poly1d(np.matmul(np.transpose(res), witness))

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

O = np.array([
[0,0,0,1,0,0,0,0],
[0,0,0,0,1,0,0,0],
[0,0,0,0,0,1,0,0],
[0,0,0,0,0,0,1,0],
[0,0,0,0,0,0,0,1],
[0,1,0,0,0,0,0,0]
])

Uw = calculPoly(L)
Vw = calculPoly(R)
Ww = calculPoly(O)
print("Uw", Uw)
print("Vw", Vw)
print("Ww", Ww)

for i in range(1, 7):    # 7 points d'interpolation
    erreur = abs(Uw(i)*Vw(i)-Ww(i))
    print(erreur)
    assert (erreur < errMax), "L'égalité n'est pas garantie"

```

## La généralisation de l'équation Uw.Vw = Ww
Nous venons de voir que l'équation est valide aux points d'interpolation. Mais cela ne s'arrête pas là. Il est possible de trouver un cas plus général à cette équation en conservant la multiplication polynomiale.

On peut constater un problème sur les degrés des polynômes. La multiplication des Polynômes Uw par Vw va nécessairement aboutir sur un polynôme de degré 10. Il faut donc annuler les degrés supérieurs au degré de Ww. Cela se fait par une polynome de degré `deg(Uw * Vw) - deg(Ww)`.  

`Uw * Vw = Ww + H` aux points d'interpolation.
Le polynome H n'a aucune chance d'annuler l'inégalité, car il est choisi de manière arbitraire.  
`(Uw * Vw) - Ww != H`

L'idée est de décomposer le polynôme H, en réduisant sa dimension pour avoir 2 termes dont un est inconnu `h` et l'autre annule l'équation aux points d'interpolation. Car justement ce sont les racines initialement testées.
`(Uw * Vw) - Ww = h * t`
$t(x) = (x-1)(x-2)(x-3)...(x-5)$
`h * t` doit être de la dimension de `(Uw * Vw)`, t peut être fabriqué commme voulu. On peut donc écrire l'équation suivante :
`((Uw * Vw) - Ww) / t = h`

Si `t` est un diviseur parfait de `((Uw * Vw) - Ww)` alors l'équation Qap fonctionne et nous avons la preuve qu'on connait le polynome initial.  
$f(x)=3x^3+5x^2+10x+3$.

En effet la probabilité de connaître un polynôme unique qui relie les signaux `U, V, et W` par un diviseur cible `t` est nulle. Vous pouvez donc vérifier cette proposition en vérifiant que le reste de la division est nul.

Dans notre exemple, [division](code/division.py), indique un reste proche de 0.
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
$h(x)=-34.09x^4+414.6x^3-1713x^2+2734x-1394$
$r(x)=0.0001015x^5-0.001524x^4+0.00865x^3-0.02295x^2+0.028x-0.01228$

A titre de comparaison la fonction résultante ((Uw*Vw)-Ww) est la suivante  
$f(x)=-34.09x^{10}+1130x^9-16380x^8+136300x^7-718700x^6+2500000x^5-5792000x^4+8785000x^3-8321000x^2+4428000x-1004000$

Le souci du système dans l'état où il se trouve est qu'il n'est pas succinct. Si on réalise un circuit complexe le système d'équation va devenir rapidement incalculable pour le **prouveur** et le **vérifieur**.
L'étape suivante consiste à porter nos équations dans un espace de calcul plus efficace. Passer sur de l'arithmétique modulaire et projeter les données dans l'espace des courbes elliptiques simplifiera les calculs.

# Rendre la preuve succincte en passant par les courbes elliptiques
## L'espace de galois
L'explication précédente se faisant dans l'espace des réels. En informatique et particulièrement en cryptographie on est vite améné à travailler dans des espaces modulaires ou espaces de Galois. C'est à dire un environnement où toutes nos équations seront exprimées en modulo d'une valeur d'un nombre premier appelé ordre. Par exemple, si on choisi l'espace de Galois de valeur 7 (ou corps de Galois 7), la matrice L et le vecteur témoins sont modifiés avec le code suivant [qapGF](code/qapGF.py). Ce code exécute la même preuve que précédemment mais dans un corps de galois d'ordre 7. 
Nous utilisons deux fonctions spécifiques : `calculPolyLagrangeGF` qui calcule les coefficients de Lagrange dans le corps et `generateT` qui fabrique le polynôme d'annulation de la puissance. 

```python
import sys
import numpy as np
import galois

def calculPolyLagrangeGF(array):
    (horizontal, vertical) = array.shape

    x = GF(np.arange(1, horizontal+1)) # x = [1, 2, 3, 4]

    tL = np.transpose(array)
    res = GF(np.zeros((vertical, horizontal), dtype=int))

    for i in range(vertical):
        r = galois.lagrange_poly(x,tL[i])
        res[i] = r.coefficients()

    return(np.transpose(res))

def generateT(size, ordre):
    '''
    (6) = (x-1)(x-2)(x-3)(x-4)(x-5)(x-6)
    '''
    result_poly = galois.Poly([1], field=ordre)  # Start with the polynomial '1' in the given field
    for val in range(1, size+1):
        # Multiply the result by (x - val) for each val in values
        result_poly *= galois.Poly([1, -val], field=ordre)
    return result_poly 

p=7
GF = galois.GF(p) 

np.set_printoptions(linewidth=np.nan)

#On part des matrices initiales que l'on contraint dans le corps par le modulo (%)
L = GF(np.array([
 [0,0,1,0,0,0,0,0],
 [0,0,1,0,0,0,0,0],
 [3,0,0,0,0,0,0,0],
 [5,0,0,0,0,0,0,0],
[10,0,0,0,0,0,0,0],
 [3,0,0,0,0,1,1,1]
]) % p)

R = GF(np.array([
[0,0,1,0,0,0,0,0],
[0,0,0,1,0,0,0,0],
[0,0,0,0,1,0,0,0],
[0,0,0,1,0,0,0,0],
[0,0,1,0,0,0,0,0],
[1,0,0,0,0,0,0,0]
]) % p)

O = GF(np.array([
[0,0,0,1,0,0,0,0],
[0,0,0,0,1,0,0,0],
[0,0,0,0,0,1,0,0],
[0,0,0,0,0,0,1,0],
[0,0,0,0,0,0,0,1],
[0,1,0,0,0,0,0,0]
]) % p)

witness = [1, 553, 5, 25, 125, 375, 125, 50]
witness = np.array(witness) % p
witness = GF(witness)

U_polys = calculPolyLagrangeGF(L)
V_polys = calculPolyLagrangeGF(R)
W_polys = calculPolyLagrangeGF(O)

Uw = galois.Poly(np.matmul(U_polys, witness))
Vw = galois.Poly(np.matmul(V_polys, witness))
Ww = galois.Poly(np.matmul(W_polys, witness))

t = generateT(len(L), GF)

h_quo = (Uw * Vw - Ww) // t
h_rem = (Uw * Vw - Ww) % t

print("t(x) = ", t,"\n")
print("\nh_quo(x) = ", h_quo)
print("h_rem(x) = ", h_rem)
if(h_rem == 0):
    print("=> La preuve est valide")
else:
    print("=> La preuve invalide")
```

Le passage par les corps de Galois ne permet pas de gagner du temps de calcul, mais de projetter les équations sur des courbes elliptiques afin de fournir une preuve plus succincte. De plus, cela permet d'obtenir un reste de division `h_hem` égal à 0 car il n'y a plus d'arrondis en calcul modulaire.

## Projection sur les courbes elliptiques
Dans la preuve QAP, le **prouveur** montre au **vérifieur** les trois polynomes Uw, Vw, Ww, ainsi que le degré des équations. Le **vérifieur** peut fabriquer le polynôme `t`, et vérifier que la division est sans reste. Mais le **vérifieur** accède quand même à ces polynômes qu'il peut alors donner à autre et se faire passer pour un **prouveur**. 

Pour palier cela, **prouveur** et **verifieur** sont mis en relation par un tier de confiance le **confident** *Trusted setup* en anglais, qui va imposer des valeurs de références uniques au deux participants. 

Le principe est le suivant. On part de l'équation : 
$Uw * Vw = Ww + HT$

Ce sont tous des polynômes, qui peuvent être évalués à n'importe quelle coordonnée. 

Prenons par exemple Uw = $4x^5 + 3x^4 + 5x^3 + 3x^2 - 4x$
En choisissant arbitrairement `x = 5`, on peut écire `4x^5 + 3x^4 + 5x^3 + 3x^2 - 4x = 15055`
Une courbe elliptique permet de fournir une valeur représentante qui montre que la solution est connue mais sans qu'on puisse remonter à l'équation source. 
$Ell(Uw(5)) = 4*Ell(5^5) + 3*Ell(5^4) + 5*Ell(5^3) + 3*Ell(5^2)-4*Elli(5)+0$

Les courbes elliptiques fonctionnent ainsi : 
On part d'un point sur la courbe, appelé G1. (En fonction des courbes considérés les points initiaux peuvent avoir plusieurs dimensions. G1 : 1 point à 2 dimensions, G2 : 2 points à 2 dimensions, G12 : 12 points à 2 dimensions.)
Si on ajoute G1 à G1, on trouve le point suivant sur la courbe. 5*G1 déplace G1 sur la courbe de 5 sauts, et 5G1 est toujours sur la courbe.

Par rapport à notre exemple : 
$15055G1 = 4*3125G1 + 3*625G1 + 5*125G1 + 3*25G1 - 4*5G1$
$15055G1 = 15055G1$
Le code python [G](code/G.py) implante cette égalité. 

```python
from py_ecc.bn128 import G1, G2, multiply, add, neg, eq
#4x^5 + 3x^4 + 5x^3 + 3x^2 - 4x = 15055

print("Uw(5) =", multiply(G1, 15055))

X5 = multiply(G1, 5**5)
X4 = multiply(G1, 5**4)
X3 = multiply(G1, 5**3)
X2 = multiply(G1, 5**2)
X1 = multiply(G1, 5)
X0 = G1

c5 = multiply(X5, 4)      #  4 * x^5
c4 = multiply(X4, 3)      #  3 * x^4
c3 = multiply(X3, 5)      #  5 * x^3
c2 = multiply(X2, 3)      #  2 * x^2
c1 = multiply(neg(X1), 4) # -4 * x 

sommeCoefs = add(add(add(add(c1,c2),c3),c4),c5)
print("Somme(coefficient) = ", sommeCoefs)

print(multiply(G1, 15055) == sommeCoefs)
```
**Remarque : dans ce dernier exemple, nous avons pris une des courbes précédentes, en changeant le dernier coefficient par son négatif pour illustrer la fonction `neg`**

Le point résulant `15055G1` 
```
(2708568011129098481813750608442309814741431019776566886222041314305674896534, 12627231381848946543670844035528126888439204587944747555252932693150421290218)
``` 
représente une valeur du polynôme en un point particulier. Il est impossible de remonter au polynôme source. Une équation polynômiale se présente sous la forme $P(x)=anx^n+a(n-1)x^(n-1)+...+a2x^2+a1x+a0$. Ce qui est important dans ces équations ce sont les coefficients ax...a0 et le degré du polynôme. En passant par les courbes elliptiques, on peu s'abstraire des puissances de x. En prenant un point de G1 au hasard, et en prenant ses puissances respectives, un tiers de confiance peut 'figer' les puissances une fois pour toute. Dans le code exemple, le point 5G1 est la valeur aléatoire initiale ('5' qui s'appelera `tau` plus loin dans le texte) et X0 à X5 sont les différentes puissances de x précalculées et figées par le **confident**.  

On arrive donc à la notion de preuve succincte :
Si `Uw * Vw = Ww + HT` sont des polynomes, le **prouveur** peux en calculer des projections équivalente sur des courbes elliptiques. 

Si 
$A = Encode(Uw, tau)$,  
$B = Encode(Vw, tau)$, 
et $C = Encode(Ww + HT, tau)$   
sont fabriqués par le **prouveur**, alors il est facile et rapide pour le **vérifieur** de controler que `A*B = C`. 
Avant cela, nous devons résoudre deux problèmes : 

1. Envoyer Uw, Vw, Ww au **confident** est une divulgation de connaissances...
2. La multiplication Uw*Vw n'a aucun sens ni dans G1, ni dans G2 il faut passer par un mécanisme de pairing. 

### Ne pas envoyer Uw au **confident**
Dans le code précédent, on constate que X0 à X5 sont des valeurs préparées et figées par **confident**. Il choisit  la valeur initiale aléatoire `tau` qu'il peut détruire / oublier dès que les puissances X0 à X5 sont calculées. Connaissant X0 à X5, il est impossible de remonter à la valeur `tau` initiale. Parallèlement, si le **prouveur** reçoit les différentes puissances (X0-X5), il peut calculer sont polynôme en continuant les déplacements sur la courbe elliptique G1. Il multiplie les puissances par les coefficients des polynômes. $P(x)=anx^n+a(n-1)x^(n-1)+...+a2x^2+a1x+a0$ devient $A = anXn+a(n-1)X(n-1)+...+a2X2+a1X1+a0X0$. Uw, Vw, Ww deviennent alors de valeurs numériques caractéristiques unique des polynômes associés. Nous les appelons A, B, C. 

Pour $HT$, le calcul se fait en appliquant $Hv(Tp)$

En résumé, le **prouveur** est capable de calculer A, B sans divulguer d'information au **confident**. 
Le **confident** envoi les coefficient X0 à Xn qui sont les points de courbe aux différentes puissances, à une coordonnée initiale inconnue de tous sauf du **confident**, qui peut être détruite une fois les X calculés.

Une partie du coût de calcul est déporté vers le **confident**, qui calcule une fois pour toute les coefficients $X0-Xn$.

Le code suivant [EncodeUwInElliptic](code/EncodeUwInElliptic.py) distingue le calcul des puissances de tau, réalisé par le **confident** du calcul de la valeur A réalisée par le **prouveur**.
```python
import sys;
from py_ecc.bn128 import G1, multiply, add, curve_order, eq, neg
import galois

# Travail du **confident**
#GF = galois.GF(curve_order)
GF = galois.GF(36209)               # BUG: must be higher order than res

tau = GF(6)                         # variable tau choisie, dans l'ordre de Galois, qui pourra être détruite

X5 = multiply(G1, int(tau**5))      # toutes les puissances de coefficients nécessaires pour tous les calculs
X4 = multiply(G1, int(tau**4))
X3 = multiply(G1, int(tau**3))
X2 = multiply(G1, int(tau**2))
X1 = multiply(G1, int(tau))
X0 = G1


# Travail du **prouveur**
# 4x^5 + 3x^4 + 5x^3 + 3x^2 + 4x 
u5 = multiply(X5, 4)
u4 = multiply(X4, 3)
u3 = multiply(X3, 5)
u2 = multiply(X2, 3)
u1 = multiply(X1, 4)
u0 = multiply(X0, 0)
encodeCoeffU=(add(add(add(add(add(u0, u1), u2),u3),u4),u5))
print("A=",encodeCoeffU)

#  !!!!   Verification a ne jamais faire : ici pour montrer que le code fonctionne
u = galois.Poly([4, 3, 5, 3, 4, 0], field=GF)
res = int(u(tau))     # tau est normalement détruit
print("res: ", res)
print("Uprouf = ", multiply(G1, res))

print(eq(multiply(G1, res), (add(add(add(add(add(u0, u1), u2),u3),u4),u5))))

```
La valeur $A=(1546263917648380985932166947985122387032060776958041831898579505785293100452, 7891785325832423556431731423973646932499847348453447787792896938638292260106)$. Représente Uw par un point de la courbe elliptique G1.

### La multiplication sur la courbe elliptique
Le produit `A * B` ne donne pas de résultat sur la courbe elliptique G1. Il faut passer par un principe de pairing. Le pairing permet de multiplier deux points sur deux courbes elliptiques G1 et G2 pour obtenir un troisième point situé sur G12. Ainsi le mapping se présente ainsi :

```python
mapping(B_G2, A_G1) == mapping(G2, C_G1) # Le mapping s'effectue sur la courbe G12, mais le point n'est pas nécessairement accessible.
```
B est un point de G2, A un point de G1, A * B indique un point C situé sur G12.
Il est a noté que le pairing ne fonctionne que sur un espace de Galois spécifique où le pairing a été vérifié. Il s'agit des courbes bn128.   

Le code suivant [testpairing](code/testpairing.py) teste le pairing `map(5*G1, 6*G2) == map(30*G1, G2)`. Ce sont les propriétés conjointes de G1, G2 et G12 qui permettent cette vérification [[cf. Bilinear Pairing](https://www.rareskills.io/post/bilinear-pairing)].

```python
from py_ecc.bn128 import multiply, G1, G2, pairing

A = multiply(G1, 5)
B = multiply(G2, 6)
C = multiply(G1, 5*6)

print(pairing(B, A) == pairing(G2, C)) # un bug de librairie python oblige de faire G2 -> G1
```

Par simulitude avec nos équations `Uw * Vw = Ww + HT` on devrait aboutir au pairing suivant. 
`pairing(Uwp_G1c, Vwp_G2c) = pairing((Wwp_G1c+HpTv_G1c), G2)`

Si cette équation est vérifiée alors le code démontre que le **prouveur** connait une équation sans en divulguer les coefficients au **vérifieur**. Les suffixes v et p indiquent d'où proviennent les données

Le code suivant [ProofArrangedFinal](ProofArrangedFinal.py) calcule la preuve proposée de bout en bout. 

```python
import sys
from py_ecc.bn128 import G1, G2, multiply, add, curve_order, pairing
import galois

GF = galois.GF(curve_order) # Attention le pairing ne fonctionne que dans ce champ.
                            # Cette ligne est très longue à s'exécuter

u = galois.Poly([14774563938491510775016323878048660684770145970280823181996287825938670734546, 3648040478639879203707734290876212514758060733402672390616367364429301415868, 10032111316259667810196269299909584415584667016857349074195010252180578894213, 7296080957279758407415468581752425029516121466805344781232734728858602830837, 8025689053007734248157015439927667532467733613485879259356008201744463116328, 21888242871839275222246405745257275088548364400416034343698204186575808495064], field=GF)
v = galois.Poly([20429026680383323540763312028906790082645140107054965387451657240804087929235, 14592161914559516814830937163504850059032242933610689562465469457717205663881, 7296080957279758407415468581752425029516121466805344781232734728858602830952, 7296080957279758407415468581752425029516121466805344781232734728858602834704, 16051378106015468496314030879855335064935467226971758518712016403488926226275, 1809], field=GF)
w = galois.Poly([11126523459851631571308589587172448170012085236878150791379920461509369318592, 3648040478639879203707734290876212514758060733402672390616367364429301416191, 13680151794899547013904003590785796930342727750260021464811377616609880307969, 7296080957279758407415468581752425029516121466805344781232734728858602837524, 8025689053007734248157015439927667532467733613485879259356008201744463107336, 3647], field=GF)
t = galois.Poly([1, 21888242871839275222246405745257275088548364400416034343698204186575808495596, 175, 21888242871839275222246405745257275088548364400416034343698204186575808494882, 1624, 21888242871839275222246405745257275088548364400416034343698204186575808493853, 720], field=GF)
h = galois.Poly([0, 18568526036276985146872367540559921700118529133019602468237309884945144207081, 8414813370729321363219173764287796867375260091715497647688420720616921933174, 2760350628837508597472185613429667469500265954941355442233051305751504736345, 1240333762737558929260629658897912255017740649356908612809564903905962484152, 19213013187503363806194067265281385911059119862587407923912868119327654122536], field=GF)

# check initial
h_quo = (u * v - w) // t
h_rem = (u * v - w) % t

print(h_quo)
print(h_rem)
if (h_rem != 0):
    print("Les équations sont cassées")
    sys.exit()
print("Les équations sont bonnes")

# La partie du **vérifieur**. Il prépare, X sur G1 et X sur G2 et T sur G2
tau = GF(123)


XG1_6 = multiply(G1, int(tau**6))
XG1_5 = multiply(G1, int(tau**5))
XG1_4 = multiply(G1, int(tau**4))
XG1_3 = multiply(G1, int(tau**3))
XG1_2 = multiply(G1, int(tau**2))
XG1_1 = multiply(G1, int(tau))
XG1_0 = G1

XG2_5 = multiply(G2, int(tau**5))
XG2_4 = multiply(G2, int(tau**4))
XG2_3 = multiply(G2, int(tau**3))
XG2_2 = multiply(G2, int(tau**2))
XG2_1 = multiply(G2, int(tau))
XG2_0 = G2

TG2_0=multiply(G2, int(t(tau)))
TG2_1=multiply(TG2_0, (int(tau)))
TG2_2=multiply(TG2_0, (int(tau**2)))
TG2_3=multiply(TG2_0, (int(tau**3)))
TG2_4=multiply(TG2_0, (int(tau**4)))

# La partie du **prouveur**
u5 = multiply(XG2_5, 14774563938491510775016323878048660684770145970280823181996287825938670734546)
u4 = multiply(XG2_4, 3648040478639879203707734290876212514758060733402672390616367364429301415868)
u3 = multiply(XG2_3, 10032111316259667810196269299909584415584667016857349074195010252180578894213)
u2 = multiply(XG2_2, 7296080957279758407415468581752425029516121466805344781232734728858602830837)
u1 = multiply(XG2_1, 8025689053007734248157015439927667532467733613485879259356008201744463116328)
u0 = multiply(XG2_0, 21888242871839275222246405745257275088548364400416034343698204186575808495064)
encodeCoeffUwG2=(add(add(add(add(add(u0, u1), u2),u3),u4),u5))

v5 = multiply(XG1_5, 20429026680383323540763312028906790082645140107054965387451657240804087929235)
v4 = multiply(XG1_4, 14592161914559516814830937163504850059032242933610689562465469457717205663881)
v3 = multiply(XG1_3, 7296080957279758407415468581752425029516121466805344781232734728858602830952)
v2 = multiply(XG1_2, 7296080957279758407415468581752425029516121466805344781232734728858602834704)
v1 = multiply(XG1_1, 16051378106015468496314030879855335064935467226971758518712016403488926226275)
v0 = multiply(XG1_0, 1809)
encodeCoeffVwG1=(add(add(add(add(add(v0, v1), v2),v3),v4),v5))

w5 = multiply(XG2_5, 11126523459851631571308589587172448170012085236878150791379920461509369318592)
w4 = multiply(XG2_4, 3648040478639879203707734290876212514758060733402672390616367364429301416191)
w3 = multiply(XG2_3, 13680151794899547013904003590785796930342727750260021464811377616609880307969)
w2 = multiply(XG2_2, 7296080957279758407415468581752425029516121466805344781232734728858602837524)
w1 = multiply(XG2_1, 8025689053007734248157015439927667532467733613485879259356008201744463107336)
w0 = multiply(XG2_0, 3647)
encodeCoeffWwG2=(add(add(add(add(add(w0, w1), w2),w3),w4),w5))

# Le **vérifieur** reçoit 
print("Le vérifieur reçoit du prouveur")
print("Uw=",encodeCoeffUwG2)
print("Vw=",encodeCoeffVwG1)
print("Ww=",encodeCoeffWwG2)
print("Les coefficients du polynôme h=", [0, 18568526036276985146872367540559921700118529133019602468237309884945144207081, 8414813370729321363219173764287796867375260091715497647688420720616921933174, 2760350628837508597472185613429667469500265954941355442233051305751504736345, 1240333762737558929260629658897912255017740649356908612809564903905962484152, 19213013187503363806194067265281385911059119862587407923912868119327654122536])

print("Il recoit également du confident, les coefficients de T[tau] pour tous les degrés de h.")
print("Il combine les coefficients de h du prouveur, avec les coeffient de T[tau] du confident.")
ht4  = multiply(TG2_4, 18568526036276985146872367540559921700118529133019602468237309884945144207081)
ht3  = multiply(TG2_3, 8414813370729321363219173764287796867375260091715497647688420720616921933174)
ht2  = multiply(TG2_2, 2760350628837508597472185613429667469500265954941355442233051305751504736345)
ht1  = multiply(TG2_1, 1240333762737558929260629658897912255017740649356908612809564903905962484152)
ht0  = multiply(TG2_0, 19213013187503363806194067265281385911059119862587407923912868119327654122536)
encodeCoeffHTG2=(add(add(add(add(ht0, ht1), ht2),ht3),ht4))

print("Le vérifieur peut alors réaliser le test suivant")
print(" Pairing(U(proof surG2), V(proof surG1) == Pairing((W(proof sur G2) + Ecode(coefh sur TG2)), G1) ")

LPairing = pairing(encodeCoeffUwG2, encodeCoeffVwG1)
RPairing = pairing(add(encodeCoeffWwG2, encodeCoeffHTG2), G1)

# Ce code fait 
# Pair(A2, B1) == Pair(C2, G1)

# La littérature fait Pair(A1, B2) == Pair(C1, G2),  mais un bug de python oblige à faire pairing(2, 1)

print("VALIDATION", LPairing == RPairing)
```

# Conclusion
L'objectif de cette présentation est de décomposer chaque étape d'une preuve Zkp/znarks/groth16 dans un code python simple, clair et réutilisable. Le code a été validé et testé afin de comprendre le déroulement de bout en bout de l'algorithme sans noyer le développeur dans les concepts mathématiques associés. Nous les considérons comme des *boites noires* fournies par les différentes bibliothèques python disponibles. 

Cependant, l'algorithme Groth16 n'est pas intégralement implanté car la dernière étape ne se déroule pas si simplement. En effet, si le *vérifieur* reçoit les trois chiffres A, B, C, il peut vérifier le pairing, mais il n'a aucune garantie que les données n'ont pas été 'inventées' par le *prouveur*. Pour palier cela, le *confident* fabrique des valeurs aléatoires propre à la preuve en cours qui va 'décaller' les valeurs A, B et C sur les différentes courbes. Ce décallage empêche le *prouveur* d'inventer complètement les valeurs. Ses calculs sont contraints par les décallages. Nous proposons dans un article suivant la réécriture de cette preuve en prenant en compte ces décalages. Nous n'avons pas proposé d'intégrer ces décalages dans ce document car il fallait revenir trop loin dans les étapes de la preuve. L'intuition initiale liée à la projection sur les courbes elliptiques devient plus complexe à percevoir. 

# Outillages
## visualisation
https://www.desmos.com/calculator?lang=fr  
https://www.geogebra.org/?lang=fr 

## Zkp, Zsnarks, Groth16
- [Under the hood of zkSNARK Groth16 protocol (part 1) | by Crypto Fairy | Coinmonks | Sep, 2023 | Medium](https://medium.com/coinmonks/under-the-hood-of-zksnark-groth16-protocol-2843b0d1558b)  
- Code python : [zkSNARK-under-the-hood/groth16.ipynb at main · tarassh/zkSNARK-under-the-hood · GitHub](https://github.com/tarassh/zkSNARK-under-the-hood/blob/main/groth16.ipynb)  
- [260.pdf (iacr.org)](https://eprint.iacr.org/2016/260.pdf)

## Fondements mathématiques pour les Zkp
- [RareSkills/zkp](https://www.rareskills.io/zk-book)

## Circuits R1CS
- [Zokrates](https://github.com/Zokrates/ZoKrates): The code is written in a language resembling Python.
- [Circom](https://github.com/iden3/circom): It uses its own domain-specific language.
- [Pequin](https://github.com/pepper-project/pequin) from the Pepper-Project: This utilizes a C-like language, similar to the gist provided above."
- https://medium.com/blockapex/a-primer-for-the-zero-knowledge-cryptography-part-ii-ecc0199d0a56
- https://medium.com/@imolfar/why-and-how-zk-snark-works-8-zero-knowledge-computation-f120339c2c55
- [Under the hood of zkSNARKs — PLONK protocol: Part 1 | by Crypto Fairy | Nov, 2023 | Medium](https://medium.com/@cryptofairy/under-the-hood-of-zksnarks-plonk-protocol-part-1-34bc406d8303)

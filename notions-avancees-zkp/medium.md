# Notions Avancées pour Comprendre les zk-SNARKs avec Groth16 :
(Explorons les Décalages Alpha, Beta, Gamma, Delta, r et s.)

Cet article fait suite à un premier exposé détaillant les bases des zk-SNARKs. Il est fortement recommandé de l'avoir lu au préalable pour pleinement appréhender le contenu de cet article, qui établit le lien entre une introduction aux zk-SNARKs et un prochain volet sur l'implémentation du protocole Groth16 en Python.

La compréhension du papier scientifique de référence de Jens Groth, exposant son idée de protocole zk-SNARK, peut sembler déroutante. Notre objectif est de partager notre vision et notre compréhension dans un langage plus accessible, tout en préservant les détails techniques essentiels pour la suite.

## 1 - Rappel sur les zk-SNARKs

Pour mieux comprendre le formalisme de Groth16, revenons sur les concepts présentés dans notre premier article. Cela nous permettra de nous familiariser davantage avec les équations et expressions utilisées dans le document de Jens Groth.

Voici ce que nous savons jusqu'à présent :
- L'objectif principal est de convaincre un vérifieur que nous possédons la connaissance d'un polynôme et que nous savons le manipuler.
- Ce polynôme subit différentes transformations. Il est d'abord converti en un circuit R1CS, puis en un modèle QAP.

- Le modèle QAP est ensuite projeté dans l'espace des courbes elliptiques pour générer des points qui simplifient la complexité de la vérification.

- À ce stade, le "trusted setup" entre en jeu pour établir un ensemble de règles contraignant le prouveur et le vérifieur, garantissant l'intégrité du processus et évitant toute tentative de triche.

Pour que le vérifieur soit convaincu de la validité de la preuve fournie par le prouveur, il doit trouver cette égalité :

![alt text](image.png)

Pour rappel:
- [A]_G1 représente l'encodage du polynôme Uw(x) dans un point appartenant à une courbe elliptique de dimension 1
- [C]_G1 représente l'encodage du polynôme Ww(x) dans un point appartenant à une courbe elliptique de dimension 1
- [B]_G2 représente l'encodage du polynôme Vw dans un point appartenant à une courbe elliptique de dimension 2

Dans l'article précédent, nous avons simplifié de nombreux processus importants que nous allons maintenant revoir ensemble afin de poser des bases solides pour aborder des notions plus complexes. Comme dans notre premier article nous allons nous appuyer sur des exemples concrets pour illustrer nos propos.

Imaginons-nous dans la position du prouveur. Notre objectif est de convaincre le vérifieur que nous connaissons un polynôme et que nous savons le manipuler. Prenons par exemple le polynôme 3x²+x+5. Nous allons construire son modèle R1CS puis son modèle QAP dans un champ de Galois, le même qui sera utilisé par le vérifieur et le "trusted setup".

Voici ce que nous avons en mémoire :

![alt text](image-1.png)

Les matrices U, V et W représentent le modèle QAP de notre équation. Pour des raisons d'esthétique, elles ont été calculées avec un ordre de Galois très petit (22091) mais ces mêmes matrices ne seront pas utilisées par la suite.

À partir de ce point, les explications divergent par rapport à l'article précédent. Comme nous l'avons présenté précédemment, nous devons demander au "trusted setup" de nous fournir un espace de travail pour travailler sur les courbes elliptiques et nous assurer que le vérifieur travaille dans les mêmes conditions.

En tant que prouveur, nous lui fournissons nos trois matrices afin qu'il puisse calculer notre espace de travail (X0, X1, X2…). Il génère un x (appelé tau auparavant) compris entre 0 et p-1, où p est l'ordre de la courbe elliptique choisie. Ensuite, il calcule x^i pour i allant de 0 à la longueur de U[0] -1.

Avant de pouvoir rendre ces données publiques au prouveur et au vérifieur, elles doivent être encodées pour cacher la valeur de x choisie. Le "trusted setup" construit donc deux tableaux où chaque x^i est transposé sur notre courbe elliptique :

$\langle [x^0]{G1}, [x^1]{G1}, [x^2]{G1}, [x^3]{G1} \rangle$
$\langle [x^0]{G2}, [x^1]{G2}, [x^2]{G2}, [x^3]{G2} \rangle$

À partir de ce moment, le prouveur peut construire A et B de la manière suivante :
<!-- ![alt text](image-2.png) -->
${[A]_1 = \sum_{i=0}^{m} a_i[u_i(x)]_1 = \sum_{i=0}^{m} a_i\sum_{j=0}^{n} u_{i,j}[x^jG_1]_1}$

${[B]_2 = \sum_{i=0}^{m} a_i[v_i(x)]_2 = \sum_{i=0}^{m} a_i\sum_{j=0}^{n} v_{i,j}[x^jG_2]_2}$

${[C]_1 = \sum_{i=0}^{m} a_i[w_i(x)]_1 + [h(x)t(x)]_1 = \sum_{i=0}^{m} a_i\sum_{j=0}^{n} w_{i,j}[x^jG_1]_1 + \sum_{i=0}^{deg(h)} h_i[x^it(x)G_1]_1}$

Une fois la preuve calculée (A, B et C), celle-ci doit être vérifiée par le vérifieur de cette manière : 
$pairing([A]₁,[B]₂) == pairing([C]₁,[G₂]₂)$


Nous remarquons que le calcul de C nécessite que le "trusted setup" nous fournisse un vecteur supplémentaire $[x^i * t(x)]_{G1}$. Revenons donc au "trusted setup" qui calcule également ce vecteur. Il définit un polynôme $t(x) = (x-1)(x-2)…(x-j)$ avec j allant de 1 à la longueur de U[0].

Ainsi, en même temps que les deux autres tableaux rendus publics, il fournit également l'accès à ce tableau :
\[ \langle [x^0 \cdot t(x)]_{G1}, [x^1 \cdot t(x)]_{G1}, [x^2 \cdot t(x)]_{G1}, [x^3 \cdot t(x)]_{G1} \rangle \]

Rappelons que la variable $x$ n'est connue que par le "trusted setup", rendant impossible pour le prouveur de calculer ce vecteur nécessaire.

Nous voilà donc au même niveau que dans l'article précédent, prêts à convaincre le vérifieur de notre connaissance de cette équation.

## 2 - Ajout de contraintes pour le prouveur (α, β)

Dans le cas où le prouveur ne serait pas honnête, il pourrait fournir au vérifieur une preuve (A, B et C) falsifiée qui passerait néanmoins le test de pairing. Il est donc nécessaire de mettre en place un mécanisme supplémentaire pour empêcher le prouveur de construire arbitrairement A et B, puis de trouver une valeur de C qui satisfait le vérifieur.

Cette contrainte supplémentaire consiste en l'ajout de deux constantes α et β, générées de la même manière que x, c'est-à-dire qu'elles prendront une valeur entre 0 et p-1.

**Voyons ensemble comment l'introduction des contraintes alpha et beta va obliger le prouveur à ne pas tricher.**

Lorsque nous reprenons depuis le début, nous savons que les matrices U, V et W doivent suivre ces équations pour que la preuve puisse ensuite être construite correctement :

<!-- ![alt text](image-3.png) -->
$$Uw(x) * Vw(x) = Ww(x) + ht(x)$$

Ici, le prouveur connaît tous les paramètres, il pourrait donc générer Uw(x) et Vw(x) de manière aléatoire et il pourrait retrouver un Ww(x) qui répondrait à cette équation. À partir de maintenant, nous introduisons alpha et beta qui ne vont plus permettre au prouveur de faire cela. Voici comment alpha et beta vont être introduits.

Alpha est ajouté à Uw(x) et beta à Vw(x). Cette somme s'explique par le décalage de points sur des courbes elliptiques, pour l'instant, nous ne travaillons pas dans cet espace, mais par la suite, nous verrons mieux ce décalage.

${(\alpha + Uw(x))(\beta + Vw(x)) = \alpha\beta + \alpha Vw(x) + \beta Uw(x) + Uw(x) * Vw(x)}$

${(\alpha + Uw(x))(\beta + Vw(x)) = \alpha\beta + \alpha Vw(x) + \beta Uw(x) + [Ww(x) + ht(x)]}$
<!-- ![alt text](image-4.png) -->

Après avoir distribué le membre de droite, nous voyons apparaître le produit Uw(x) et Vw(x) que nous avons déjà rencontré dans l'équation précédente. Par substitution, nous remplaçons ce produit par Ww(x) + ht(x).

***À chaque étape de calcul, nous vérifions le déroulement de cette démonstration avec un code Python.***

Ajoutons une étape, le passage sur les courbes elliptiques. Pour cela, nous convertissons chaque terme par un point sur une courbe elliptique, ils sont représentés par la notation […]_1 et […]_2. De plus, la multiplication n'existant pas dans l'espace des courbes elliptiques, nous utilisons la fonction de pairing notée "•" ici.

Ici nous devons choisir un x, pour faire l'évaluation des polynomes pour ensuite faire la transposition dans les coubres élliptiques:

${( [\alpha]_1 + [U_w(x)]_1 ) \bullet ( [\beta]_2 + [Vw(x)]_2) = [\alpha]_1 \bullet [\beta]_2}$
${ + ( \textcolor{red}\beta \times [Uw(x)]_1 ) \bullet [G_2]_2}$
${+( \textcolor{red}\alpha  \times [Vw(x)]_1 ) \bullet [G_2]_2}$
${+ [W_w(x)]_1 \bullet [G_2]_2}$
${+ [ ht(x) ]_1 \bullet [G_2]_2
}$

<!-- ![alt text](image-5.png) -->

Voici ce que nous remarquons : tous les éléments de cette équation sont des points sur des courbes elliptiques, sauf à deux moments. Nous remarquons que nous avons besoin d'alpha et beta, qui n'ont pas été transposés par un point sur une courbe elliptique.

En quoi l'introduction d'alpha et beta va résoudre le problème du prouveur malhonnête ? Il est important de se rappeler que le prouveur va construire ses matrices U, V et W, et que le confident va lui permettre de les convertir en des points sur les courbes elliptiques grâce à un ensemble de règles que nous avons déjà vues (il génère un x qui élève à des puissances i, qu'il encode dans des points de CE…). Le confident va fournir au prouveur alpha et beta encodés dans des points sur CE également, mais ce confident ne va jamais fournir publiquement la valeur d'alpha et beta en clair.

Donc à partir de cela, le prouveur, ne connaissant pas la valeur d'alpha et beta en clair, il ne peut plus construire "un nouveau C" qui répondrait à cette dernière équation.

## 3 - Ajout de contraintes pour le proveur (γ, δ)
https://kayleegeorge.github.io/math110_WIM.pdf 
**Le rôle des autres éléments du champ secret
γ, δ sont utilisés pour rendre la contribution du public indépendante des autres composants témoins.**

(Pour éviter les contrefaçons, nous proposons une approche utilisant des données publiques. Nous partons du principe que les évaluations polynomiales βu₀(τ), αw₀(τ) et w₁(τ) sont utilisées par le vérificateur, et non par le prouveur. Cependant, il est techniquement possible pour le prouveur d'utiliser w₀(τ) et w₁(τ) pour créer une fausse preuve, bien que cela soit difficile à réaliser.

Pour contrer cette possibilité, nous introduisons un élément de sécurité en divisant w₀(τ) et w₁(τ) par une variable secrète γ du côté du vérificateur, et par une variable différente δ du côté du prouveur. Les versions cryptées de ces variables [γ] et [δ] sont rendues disponibles afin que le vérificateur et le prouveur puissent les utiliser pour annuler leurs contributions respectives, en garantissant l'intégrité du processus si les parties agissent de manière honnête.

Étape de vérification avec γ et δ
Au lieu d'apparier avec G₂ à l'étape de vérification, nous apparions avec [γ] et [δ].

Étape de vérification avec delta gamma et entrées publiques
Les termes [γ] et [δ] s'annuleront si le prouveur a réellement utilisé les polynômes issus de la configuration de confiance. Le prouveur (et le vérificateur) ne connaissent pas l'élément de champ qui correspond à [δ], donc ils ne peuvent pas provoquer l'annulation des termes à moins d'utiliser les valeurs de la configuration de confiance.

Si le prouveur utilise les évaluations de polynômes provenant de la partie des entrées publiques du témoin, les termes γ et δ ne s'annuleront pas.)

## 4 - Ajout de contraintes par le prouveur (r, s)

Pour garantir un véritable secret de la connaissance : r et s
Notre schéma n'est pas encore véritablement secret de la connaissance. Si un attaquant parvient à deviner notre vecteur de témoin (ce qui est possible s'il existe seulement une petite plage d'entrées valides, par exemple, des votes secrets provenant d'adresses privilégiées), alors il peut vérifier si sa supposition est correcte en comparant sa preuve construite à la preuve originale.

Pour remédier à cela, nous introduisons un autre décalage aléatoire, mais cette fois-ci lors de la phase de preuve au lieu de la phase de configuration.

Le prouveur échantillonne deux éléments de champ aléatoires r et s et ajuste leurs valeurs en conséquence.

Remarquez que nous devons inclure [β]₁ et [δ]₁ comme partie de la configuration de confiance pour que cela fonctionne.

Il est demandé au lecteur de montrer que l'ajout de r et s de cette manière n'altère pas l'équilibre de l'équation pour le vérificateur, quelles que soient les valeurs de r et s indiquées.


# Preuves à divulgation nulle de connaissance (ZKP)

Les preuves à divulgation nulle de connaissances (Zero Knowledge Proofs) couvrent un nouveau concept dans le domaine de la cryptographie. Elles permettent à une partie ; le **prouveur** ; de montrer à une autre partie ; le **vérifieur** ; qu'une **affirmation** est vraie, sans révéler d'information supplémentaire.

### Exemples simples

Exemple 1 (Où est Charlie ?)
---------
Dans le jeu "où est Charlie ?", il faut retrouver les coordonnées d'un personnage appelé Charlie dans un dessin rempli de détails. Dans la solution de base, le prouveur est celui qui indique où est le personnage, le vérifieur peut voir sur le dessin que Charlie est au bon endroit indiqué.

Dans une approche ZKP le prouveur peut montrer au vérifieur qu'il sait où se trouve Charlie sans divulguer sa position.

Pour cela, il recouvre l'image d'un cache noir largement plus grand que le dessin. C'est à dire au moins 3 fois la dimension de l'image sur  les deux dimensions. Dans ce cache, un trou est fait de la dimension du personnage de Charlie et positionne ce trou sur "l'image de Charlie". Le cache recouvre largement l'image et ne divulgue que Charly, mais pas sa position dans l'image. Le cache couvrant les coordonnées de l'image. Le vérifieur voit charly à travers le trou, mais ne sais pas à quelles coordonnées dans l'image il se trouve. En repartant le vérifieur sais que le prouveur à trouvé Charlie, mais le vérifieur ne sais pas où il se trouve. Il y a eu preuve de l'affirmation sans divulgation de la coordonnée.

Exemple 2 (Résolution de sudoku)
---------
Le jeu de sudoku consiste à répartir des chiffres de 1 à 9 dans une grille 9x9 formée de 9 pavés de 3x3. Pour être résolue la grille doit comporter tous les chiffres uniques de 1 à 9 sur toutes les lignes, toutes les colonnes et tous les pavés de 9 cases. Pour contraindre le système, la grille est initialement peuplée de valeurs qui par déduction amènent à une solution unique. Le jeu consiste à répartir les 27 séries de 9 valeurs de toutes les zones de la grille (lignes, colonnes, pavés). Dans la solution de base, le prouveur est celui qui montre que tous les chiffres sont présents et répartis dans la grille.

Dans une approche ZKP, le prouveur peut montrer au vérifieur qu'il connait la solution sans divulguer la répartition des chiffres.

Pour cela, il ne marque pas la solution directement sur la grille, mais sur des étiquettes mobiles qu'il colle sur les cases vides de la grilles. Chaque case contient une étique avec la valeur solution. Ces étiquettes sont retournée afin que le vérifieur ne puisse pas voir les valeurs solution. Pour que la preuve ZKP fonctionne, le vérifieur pose 18  questions. Chaque question consiste à demander l'ensemble des étiquettes constituant une des zone de répartition (ligne, colonne ou pavé). Le prouveur prend les étiquettes les mélange caché et dévoile au vérifieur que les 9 chiffres sont bien présents de manière unique. Puis il replace les étiquettes face cachées sur leur emplacement. En répétant ce processus 18 fois, le vérifier est convaincu à 100% que le prouver connait bien la solution à la grille, mais le vérifier ne connait pas la position des différentes valeurs dans la grille.

Cette preuve est dite interactive, car elle peut se terminer avant la fin des 18 intérations. En effet, au fur et à mesure des itérations le vérifier devient de plus en plus convaincu que le prouver a bien résolu la grille.

Ces deux exemples donnent une intuition sur le principe de fonctionnement des approches par ZKP. Dans le cadre général il s'agit d'arriver à montrer qu'on connait la réponse à une question en révélant des valeurs qui n'ont pas de correlation directe avec la solution. "Charly est là, mais je n'ai pas sa coordonnée", "les chiffres sont là mais je n'ai pas vu l'organisation".

Il existe de nombreux exemples plus ou moins intuitifs sur les méchanismes de ZKP. Dans le domaine de la crypto, les techniques tournent autour de la résolution de polynomes de degrés n. Le principe est de montrer qu'on connait la solution d'un système d'équations sachant que la complexité du système rend improbable le fait de trouver la solution par tirage aléatoire. Par exemple, si vous savez qu'il s'agit d'un ensemble de 10 courbes, et que le prouveur annonce qu'il pense que toutes les courbes de cet ensemble passent par des points de coordonnées (12, 100), (20, 230), (32, 430), (1233,2301), (124, 131389), (1212,101281818) et (13123, 12239191281), il y a de fortes chance qu'il connaisse l'ensemble. Le mécanisme  zkSNARK consiste à construire cet ensemble de courbes afin de permettre à un prouveur qu'il connait une solution type que le verifier peut facilement controler.
Pour ceci le vérifier connait une courbe de référence publique (x-1)(x-2)(x-3).... Cette courbe coupe l'axe des x aux coordonnées (0, 1), (0, 2) (0, 3) (0, 4). D'autre part le vérifier possède un certain nombre de coefficient de courbes qui sont indirectement liés au système d'équation initial. Le prouver fourni un vecteur solution de valeurs [x1,...xn] que le vérifier peu appliquer à son système de courbe. Le vérifier peut alors controler que sa courbe publique est un diviseur exact de la courbe déduite à partir du vecteur solution appliqué au système de coefficients.

Le prouver indique qu'il connait une solution [x1,...xn], sans que le vérifieur puisse remonter aux courbes initiales.


Voici des exemples simplifier :

- Caverne l'ali baba

- Le problème du daltonien et des boulles de couleur

### Applications //SFR pour moi c'est inutile pour l'instant

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

---------

### zk-SNARK

Les zk-SNARKs sont des preuves à divulgation nulle de connaissance succinctes et non interactives. Ils sont utilisés pour prouver qu'une information est vraie sans révéler l'information elle-même. Les zk-SNARKs sont utilisés dans de nombreuses blockchains, notamment Zcash, Ethereum et Tezos.

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

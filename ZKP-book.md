# Preuves à divulgation nulle de connaissance (ZKP)

Les preuves à divulgation nulle de connaissance sont un concept fascinant dans le domaine de la cryptographie. Elles permettent à une partie (le prouveur) de montrer à une autre partie (le vérificateur) qu'une affirmation est vraie, sans révéler d'information supplémentaire. 

## Introduction aux ZKP?

Les ZKP sont des méthodes cryptographiques qui permettent à une personne de prouver qu'elle connaît une valeur particulière sans révéler cette valeur. En d'autres termes, elles permettent de prouver une connaissance sans révéler cette connaissance.

### Exemple simple

Prenons l'exemple d'un jeu de devinette où Alice veut prouver à Bob qu'elle connaît un secret, mais sans le lui révéler. Avec un ZKP, Alice pourrait convaincre Bob qu'elle connaît le secret sans jamais avoir à le lui divulguer. Voici des exemples simplifier : 

- Caverne l'ali baba

- Le problème du daltonien et des boulles de couleur

- Ou est Charlie

### Applications

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

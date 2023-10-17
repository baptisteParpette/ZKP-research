- [Preuves à divulgation nulle de connaissance (ZKP)](#preuves-à-divulgation-nulle-de-connaissance-zkp)
  - [Introduction aux ZKP?](#introduction-aux-zkp)
    - [Exemple simple](#exemple-simple)
    - [Applications](#applications)
    - [Comment cela fonctionne-t-il?](#comment-cela-fonctionne-t-il)
    - [zk-SNARK](#zk-snark)
      - [Fonctionnement technique :](#fonctionnement-technique-)
          - [Traduction d'un probleme en un circuit arithmetique :](#traduction-dun-probleme-en-un-circuit-arithmetique-)
          - [Convertion circuit en R1CS :](#convertion-circuit-en-r1cs-)
          - [Convertion R1CS en QAP :](#convertion-r1cs-en-qap-)
        - [Pour la suite:](#pour-la-suite)
        - [Ressources :](#ressources-)
          - [Point de départ vers beaucoup de ressource :](#point-de-départ-vers-beaucoup-de-ressource-)
          - [3 videos que modelise un problème en circuit arithmetique et le converti en R1CS et QAP et ECC:](#3-videos-que-modelise-un-problème-en-circuit-arithmetique-et-le-converti-en-r1cs-et-qap-et-ecc)
          - [Les 3 articles de Vitalik Buterin sur les zk-SNARKs :](#les-3-articles-de-vitalik-buterin-sur-les-zk-snarks-)
          - [Un article sur les elliptic curves :](#un-article-sur-les-elliptic-curves-)
          - [Eli Ben-Sasson sur les zk-SNARKs :](#eli-ben-sasson-sur-les-zk-snarks-)
          - [Utilisation de libsnark pour les zk-SNARKs :](#utilisation-de-libsnark-pour-les-zk-snarks-)

# Preuves à divulgation nulle de connaissance (ZKP)

Les preuves à divulgation nulle de connaissance sont un concept fascinant dans le domaine de la cryptographie. Elles permettent à une partie (le prouveur) de montrer à une autre partie (le vérificateur) qu'une affirmation est vraie, sans révéler d'information supplémentaire[^1].

## Introduction aux ZKP?

Les ZKP sont des méthodes cryptographiques qui permettent à une personne de prouver qu'elle connaît une valeur particulière sans révéler cette valeur. En d'autres termes, elles permettent de prouver une connaissance sans révéler cette connaissance.

### Exemple simple

Prenons l'exemple d'un jeu de devinette où Alice veut prouver à Bob qu'elle connaît un secret, mais sans le lui révéler. Avec un ZKP, Alice pourrait convaincre Bob qu'elle connaît le secret sans jamais avoir à le lui divulguer.

### Applications

Les ZKP ont de nombreuses applications, notamment :

- **Authentification** : Prouver que vous connaissez un mot de passe sans le révéler.
- **Transactions privées** : Effectuer des transactions sur une blockchain sans révéler les montants ou les participants.
- **Vote électronique** : Voter sans révéler son choix, tout en prouvant que le vote a été effectué correctement.

### Comment cela fonctionne-t-il?

Sans entrer dans les détails techniques, le fonctionnement des ZKP repose sur des problèmes mathématiques complexes qui sont difficiles à résoudre sans connaître certaines informations secrètes. Le prouveur utilise ces informations secrètes pour générer une preuve, et le vérificateur peut alors vérifier cette preuve sans jamais connaître les informations secrètes.



[^1]: Pour une explication plus technique des ZKP, voir l'article de [nom de l'auteur](URL).

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





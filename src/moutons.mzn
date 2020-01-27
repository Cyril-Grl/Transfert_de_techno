int: nb_m = 2;

int: vide = 0;
int: blanc = 1;
int: noir = 2;

int: taille = 2*nb_m + 1;

int: max_etapes = 50;

array[1..max_etapes, 1..taille] of var vide..noir: etat;

var 1..max_etapes: total_steps;

array[1..max_etapes] of var set of 1..taille: transfered;

solve minimize total_steps;

constraint
  forall(i in 1..taille) (
    % initilisation
    ((i <= nb_m) -> etat[1,i] = blanc)
    /\
    ((i = nb_m + 1) -> etat[1,i] = vide)
    /\
    ((i > nb_m + 1) -> etat[1,i] = noir)
    /\
    % etat final
    ((i <= nb_m) -> etat[total_steps,i] = noir)
    /\
    ((i = nb_m + 1) -> etat[total_steps,i] = vide)
    /\
    ((i > nb_m + 1) -> etat[total_steps,i] = blanc)
  )
  /\
  transfered[1] = 1..taille
;

constraint
  forall(e in 2..max_etapes)(
    % on bouge 1 mouton par tour (avec vide)
    sum(i in 1..taille)(bool2int(etat[e-1,i] != etat[e,i])) = 2
    /\
    % on a toujours le meme nombre de moutons
    sum(i in 1..taille)(bool2int(etat[e-1,i] = blanc)) = nb_m
    /\
    sum(i in 1..taille)(bool2int(etat[e-1,i] = noir)) = nb_m
    /\
    sum(i in 1..taille)(bool2int(etat[e-1,i] = vide)) = 1
  )
;


constraint
  forall(e in 2..max_etapes)(
    forall(i1,i2,i3 in 3..taille where i1 = i3-2 /\ i2 = i3-1)(
      % se deplacer d une case vers la droite pour les blancs
      (((etat[e-1,i1] = blanc /\ etat[e-1,i2] = vide) -> (etat[e,i1] = vide /\ etat[e,i2] = blanc))
      xor
      % se deplacer d une case vers la droite pour les blancs
      ((etat[e-1,i2] = blanc /\ etat[e-1,i3] = vide) -> (etat[e,i2] = vide /\ etat[e,i3] = blanc)))
      xor
      % se deplacer d une case vers la gauche pour les noirs
      (((etat[e-1,i2] = noir /\ etat[e-1,i1] = vide) -> (etat[e,i2] = vide /\ etat[e,i1] = noir))
      xor
      % se deplacer d une case vers la gauche pour les noirs
      ((etat[e-1,i3] = noir /\ etat[e-1,i2] = vide) -> (etat[e,i3] = vide /\ etat[e,i2] = noir)))
      xor
      % sauter par dessus un mouton pour les blancs
      (((etat[e-1,i1] = blanc /\ etat[e-1,i2] != vide /\ etat[e-1,i3] = vide) -> (etat[e,i1] = vide /\ etat[e,i2] = etat[e-1,i2] /\ etat[e,i3] = blanc))
      xor
      % sauter par dessus un mouton pour les noirs
      ((etat[e-1,i1] = vide /\ etat[e-1,i2] != vide /\ etat[e-1,i3] = noir) -> (etat[e,i1] = noir /\ etat[e,i2] = etat[e-1,i2] /\ etat[e,i3] = vide)))
      xor
      % ne pas bouger
      (((etat[e-1,i1] = blanc \/ etat[e-1,i1] = noir) /\ (etat[e-1,i2] = blanc \/ etat[e-1,i2] = noir) /\ (etat[e-1,i3] = blanc \/ etat[e-1,i3] = noir)) -> (etat[e,i1] = etat[e-1,i1] /\ etat[e,i2] = etat[e-1,i2] /\ etat[e,i3] = etat[e-1,i3]))
    )
  )
;


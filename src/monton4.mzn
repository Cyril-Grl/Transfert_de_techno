
int: nb_m = 1;
int: moutons = 2*nb_m;
int: taille = moutons+1;
int: max_etapes = 6;
var 1..max_etapes: total_steps;

enum pion = {noir, blanc, vide};

array[1..max_etapes] of var 1..moutons: transfered;
array[1..max_etapes] of var 1..taille: place_vide;

array[1..max_etapes, 1..taille] of var pion: action;

solve minimize total_steps;

constraint
   forall(i in 1..taille) (
     ((i <= nb_m) -> action[1,i] = blanc)
     /\
     ((i = nb_m+1) -> action[1,i] = vide)
     /\
     ((i > nb_m+1) -> action[1,i] = noir)
     /\
     ((i <= nb_m) -> action[total_steps,i] = noir)
     /\
     ((i = nb_m+1) -> action[total_steps,i] = vide)
     /\
     ((i > nb_m+1) -> action[total_steps,i] = blanc)
   )
   /\
   transfered[1] = nb_m + 1
;

constraint
  forall(t in 2..max_etapes)(
    sum(i in 1..taille)(bool2int(action[t,i] = blanc)) = nb_m
    /\
    sum(i in 1..taille)(action[t,i] = vide) = 1
    /\
    sum(i in 1..taille)(action[t,i] = noir) = nb_m
  )
;

constraint
  forall(t in 2..max_etapes) (
    forall(i in 1..taille)(
      action[t-1,i] = vide -> place_vide[t-1] = i
    )
    )
;

constraint
  forall(t in 2..max_etapes) (
    (
      ((action[t-1,place_vide[t-1]-1] = blanc /\  action[t,place_vide[t]] = blanc /\ action[t,place_vide[t]-1] = vide /\ transfered[t] = (place_vide[t]))
      xor
      (action[t-1,place_vide[t-1]-2] = blanc /\  action[t,place_vide[t]] = blanc /\ action[t,place_vide[t]-2 ] = vide /\ transfered[t] = (place_vide[t])))
      xor
      ((action[t-1,place_vide[t-1]+1] = noir /\  action[t,place_vide[t]] = noir /\ action[t,place_vide[t]+1] = vide /\ transfered[t] = (place_vide[t]))
      xor
      (action[t-1,place_vide[t]+2] = noir /\ action[t,place_vide[t]] = noir /\ action[t,place_vide[t]+2] = vide /\ transfered[t] = (place_vide[t])))
      )
      \/
      exists(e in 1..taille)(
        transfered[t] != e
      )
  )
;

constraint
  forall(t in 2..max_etapes) (
    exists(e in 1..taille)(
      transfered[t] = e
      /\
      transfered[t-1] != e
    )
  )
;
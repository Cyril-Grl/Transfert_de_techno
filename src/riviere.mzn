% Traversée de la rivière

% Trois buffles et trois lions doivent traverser une rivière sur un radeau qui ne peut supporter que deux animaux. A chaque traversée au moins un animal doit se trouver sur le radeau. Sur chaque rive, si le nombre de lions est strictement supérieur au nombre de buffles alors ceux-ci recouvrent leur instinct de prédateurs et dévorent les buffles. Il faut donc trouver un ordre de passage permettant à tous les animaux de se retrouver sur l’autre rive.

int: max_etapes;
int: nb_bison;
int: nb_lion = nb_bison;
int: nb_animaux = nb_bison*2;

int: max_num_to_cross = 2;
int: A = 1;
int: B = 2;
array[1..max_etapes, 1..nb_animaux] of var A..B: actions;
array[1..max_etapes] of var A..B: position_radeau;
var 1..max_etapes: total_steps;
array[1..max_etapes] of var set of 1..nb_animaux: transfered;


constraint
   % initilisation
   forall(i in 1..nb_animaux) (
      actions[1,i] = A
   )
   /\
   position_radeau[1] = A
   /\
   transfered[1] = 1..nb_animaux
;

constraint
  forall(t in 2..max_etapes) (
    (
      ( (position_radeau[t] = B ->
      (
        sum(i in 1..nb_bison)(bool2int(actions[t,i] = A))  % nb bisons cote A
        >=
        (
          (sum(i in nb_bison+1..nb_animaux)(bool2int(actions[t,i] = A))) % nb lions cote A
        )
      )
      )
      /\
      (position_radeau[t] = A ->
      (
        sum(i in 1..nb_bison)(bool2int(actions[t,i] = A))  % nb bisons cote B
        >=
          sum(i in nb_bison+1..nb_animaux)(bool2int(actions[t,i] = A))
          -
          (card(transfered[t] intersect nb_bison+1..nb_animaux))
      )
      )
    )
  )
    /\
    ( (position_radeau[t] = B ->
      (
        sum(i in 1..nb_bison)(bool2int(actions[t,i] = B))  % nb bisons cote B
        >=
        (
          (sum(i in nb_bison+1..nb_animaux)(bool2int(actions[t,i] = B)))
          -
          (card(transfered[t] intersect nb_bison+1..nb_animaux)) % nb lions cote B
        )
      )
      )
      /\
      (position_radeau[t] = A ->
      (
        sum(i in 1..nb_bison)(bool2int(actions[t,i] = B))  % nb bisons cote B
        >=
          sum(i in nb_bison+1..nb_animaux)(bool2int(actions[t,i] = B))
      )
      )
    )

  )
;

constraint
  % les transferts
  forall(t in 2..max_etapes) (
    % position de la torche à alterner
    exists(place in A..B) (
      % où était la torche à l'étape précédente
      position_radeau[t-1] = place
      /\ % la torche change de rive
      position_radeau[t] != position_radeau[t-1]
      /\
      %pas plus de deux personnes en même temps
      (card(transfered[t])in 1..max_num_to_cross)
      /\
      % liens transferts actions
      forall(i in 1..nb_animaux) (
        ((i in transfered[t]) <-> (
          actions[t-1,i] = place /\
          actions[t-1,i] != actions[t,i]
        ))
      /\
      (not(i in transfered[t]) <-> actions[t-1,i] = actions[t,i])
      )
    ) % fin du exists
  )
;

constraint
  % le but à atteindre
  exists(t in 2..max_etapes) (
    % tous sur la rive B
    forall(i in 1..nb_animaux) (
      actions[t, i] = B
    )
    /\
    position_radeau[t] = B
    /\
    total_steps = t
   )
;



solve minimize total_steps;
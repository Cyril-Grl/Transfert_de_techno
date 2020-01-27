%
% Traversée du pont
%
% Quatre personnes (1,2,3, et 4)  veulent traverser une rivière dans la nuit. Il y a un pont étroit de la rive A à la rive B qui ne peut supporter que deux personnes à la fois. Comme c'est la nuit, une torche doit être utilisée lors de la traversée du pont. La personne 1 peut traverser le pont en 1 minute, 2 en 2 minutes, 3 en 5 minutes, et 4 en 8 minutes. Lorsque deux personnes traversent le pont ensemble, elles doivent se déplacer au rythme de la personne la plus lente. Peuvent-ils traverser en 15 minutes ou moins ?

int: nb_seaux;
int: max_etapes;

array[1..nb_seaux] of int: contenance_max;
array[1..nb_seaux] of int: contenu;
array[1..nb_seaux] of int: fin;

int: contenu_max = sum(i in 1..nb_seaux)(contenu[i]);

array[1..max_etapes, 1..nb_seaux] of var int: etat;

var 1..max_etapes: n_etape_fin;

solve minimize n_etape_fin;

constraint
    forall(i in 1..nb_seaux)(
    % le premier etat contient le contenu
    etat[1,i] = contenu[i]
    /\
    % le dernier etat contient le contenu de fin
    (etat[n_etape_fin,i] = fin[i])
  )
;

constraint
  % il ne manque pas d'eau!
  forall(e in 1..max_etapes)(
    contenu_max = sum(i in 1..nb_seaux)(etat[e,i])
  )
;

constraint
  % ne pas depasser la contenance max de chaque seau
  forall(e in 1..max_etapes)(
    forall(i in 1..nb_seaux)(
      ((etat[e,i] <= contenance_max[i]) /\ (etat[e,i] >= 0))
    )
  )
;

constraint
  % on a que deux seaux qui changent
  forall(e in 2..max_etapes)(
    sum(i in 1..nb_seaux)(bool2int(etat[e-1,i] != etat[e,i])) = 2
  )
;

constraint
  % on vide un seau dans l'autre a chaque tour
  forall(e in 2..max_etapes)(
    forall(i1,i2 in 1..nb_seaux where i1!=i2)(
      % si le seau 1 est vide dans le seau 2
      ((etat[e-1,i1] > etat[e,i1]) /\ (etat[e-1,i2] < etat[e,i2]))
      ->
      % alors soit le premier est vide au moment courant, soit le deuxieme a atteint son max
      ((etat[e,i1] = 0) \/ (etat[e,i2] = contenance_max[i2]))
    )
  )
;

# Transfert_de_techno

Jeux des seaux d’eau (cf. film Die Hard 3)

On dispose de N seaux d’eau dont les capacités respectives sont connues. Partant d’une situation initiale donnant le remplissage de chacun des seaux, il faut arriver à une situation finale donnée par une série de transfertsd’eau entre les seaux. Tout transfert d’eau s’effectue sans pertes et consiste à vider un seau X pour en remplir un autre Y. Un transfert de X à Y n’a pas de sens si X est vide ou Y est rempli à bord. On ne dispose pas d’instruments de mesure.

Exemple:

On dispose de trois seaux d’eau A, B, C de capacités respectives 8 litres, 5 litres et 3 litres. Dans l’état de départ, A est rempli à ras bord, B et C sont vides. Combien faut-il opérer de transferts d’eau pour que A et B contiennent chacun 4 litres et que C soit vide ?


---
# Installation

Sous Linux:
    
Pour MiniZinc:

    snap install minizinc --classic

puis dans l'env:

    pip install minizinc

sudo apt-get install python3-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev


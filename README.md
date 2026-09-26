# Video ou images vers GIF ou WEBP animé 
<br>

Programmes écrit en python.<br>

## video_to_gif<br>

Permet générer un GIF animé à partir d'une vidéo<br>
version 0.16 => gif<br>
version 0.17 => gif et webp<br><br>

<br>
Visu de video_to_gif_0.16_
<img alt="gif_crator" src="https://github.com/fifi82/Gif-creator/blob/main/visu_0.16.jpg" /><br>

L'interface utilise "Tkinter"<br>
L'ouverture des vidéos et l'extraction des images utilise "moviepy" pour video_to_gif <br>
Le traitement des images utilise "PIL" <br>
<br>
"loop" permet si il est à 0 de lire l'animation en permanence, si non il lit l'animation autant de fois la valeur sélectionnée.<br>
"pingpong" permet de lire l'animation dans les deux sens, du début vers la fin puis de la fin vers le début.<br>
"[A] Début du GIF" et "[B] Fin GIF" permet de choisir une portion de la vidéo, un curseur rouge indique la sélection.<br>
"Supp hors sélection" efface les images en dehors de la sélection.<br>
"Supprime la sélection" efface les images de la sélection.<br>
"Ouvrir une vidéo" charge une vidéo en mémoire, évitez les grosses vidéos, utilisez AviDemux par exemple pour découper une partie de la vidéo.<br>
"Sauvegarde en GIF" sauvegarde la sélection en GIF.<br>
"Lecture en marche" permet de lire ou de stopper l'animation.<br>
"le curseur marron" permet de modifier la taille du GIF en fonction de la taille de la vidéo chargée et valider avec le bouton à sa droite.<br>
"curseur bleu clair" "pas de lecture(step)" permet de lire toute les n images, si la valeur est négative l'animation est lue à l'envers.br>
"curseur turquoise" "temps par image en millisecondes" permet de régler le temps de chaque images, (identique pour toutes les images).<br>
Petits problèmes:
- la vitesse de lecture dans l'éditeur n'est pas tout à fait la même que sur le gif de sortie, surtout dû a la dimension trop importante du gif
  
<hr><br>

## images_to_gif<br>

créer des GIF animés à partir de plusieurs images<br>
<img alt="images_to_gif" src="https://github.com/fifi82/Gif-creator/blob/main/visu_images_to_gif.jpg" /><br>

<hr><br>

## gif editor<br>

éditer les gif><br>
<br><br>

**README**

**Nom du projet:** QCM Scanner



**Description:** Ce projet utilise OpenCV et l'intelligence artificielle pour scanner un QCM à partir d'une image ou d'une vidéo. Le code utilise les étapes suivantes pour scanner un QCM :

1. **Importation des bibliothèques et des données:** Le code importe les bibliothèques OpenCV et NumPy, ainsi que les données du QCM, qui sont composées des questions, des choix et des réponses correctes.
2. **Prétraitement de l'image QCM:** Le code redimensionne l'image, la convertit en niveaux de gris et applique un flou gaussien.
3. **Détection des contours rectangulaires:** Le code utilise le filtre Canny pour détecter les contours rectangulaires dans l'image.
4. **Extraction des points de repère des rectangles:** Le code extrait les points de repère des deux plus grands rectangles, qui correspondent au QCM et à la zone de note.
5. **Déplacement des rectangles:** Le code utilise la distorsion de la perspective pour déplacer les rectangles dans leur position d'origine.
6. **Application d'un seuil à l'image:** Le code applique un seuil à l'image pour séparer les réponses des autres éléments de l'image.
7. **Détection des cercles de réponses:** Le code détecte les cercles dans l'image, qui correspondent aux réponses des questions.
8. **Calcul des réponses correctes:** Le code compare les réponses détectées aux réponses correctes pour calculer la note du QCM.
9. **Affichage des réponses correctes et de la note:** Le code affiche les réponses correctes et la note du QCM sur l'image.

**Enregistrement de l'image scannée:** Si vous souhaitez enregistrer l'image scannée, vous pouvez appuyer sur la touche `s` lorsque l'image est affichée.

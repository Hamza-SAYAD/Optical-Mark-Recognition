# Le fichier actuel contient des fonctions utilitaires qui seront utilisées dans le fichier principal pour effectuer différentes opérations de traitement d'image.

# Importation des bibliothèques nécessaires
import os
import cv2
import numpy as np
import streamlit as st


def stackImages(imgArray, scale, labels=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])

    rowsAvailable = isinstance(imgArray[0], list)
    # la largeur et la longueur de la première image du tableau  imgArray
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]

    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):

                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                # les convertit en couleur si elles sont en niveaux de gris,
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        # une image vide
        imageBlank = np.zeros((height, width, 3), np.uint8)

        hor = [imageBlank] * rows

        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])

            #
        ver = np.vstack(hor)


    #      si le tableau  imgArray  ne contient pas de listes d'images mais juste des images individuelles
    else:

        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)

            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)

        ver = hor
    # si la liste  labels  n'est pas vide.
    if len(labels) != 0:
        # la largeur et la longueur de chaque image de la liste  labels .
        eachImgWidth = int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        for d in range(0, rows):
            for c in range(0, cols):
                cv2.rectangle(ver, (c * eachImgWidth, eachImgHeight * d),
                              (c * eachImgWidth + len(labels[d][c]) * 13 + 27, 30 + eachImgHeight * d),
                              (255, 255, 255), cv2.FILLED)

                cv2.putText(ver, labels[d][c], (eachImgWidth * c + 10, eachImgHeight * d + 20),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 255), 2)

    return ver


# Définition de la fonction reorder qui réorganise les points d'un rectangle,
# La fonction prend en entrée les points d'un rectangle et renvoie les points réorganisés.
def reorder(myPoints):
    # REORDONNER LES POINTS POUR OBTENIR CELUI D'ORIGINE QUI EST LA PLUS PETITE SOMME DE CHAQUE POINT ET CELA CONTINUE JUSQU'À ATTEINDRE LA PLUS GRANDE SOMME
    # convertit la liste de points en un tableau NumPy à deux dimensions.
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    # la somme des coordonnées de chaque point.
    add = myPoints.sum(1)

    # obtenir le point d'origine (le point avec la plus petite somme de coordonnées) en premier
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    # puis les autres points dans le sens des aiguilles d'une montre.
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    # renvoie des nouveaux points ordonnés
    return myPointsNew


# Définition de la fonction rectContour qui prend en entrée les contours et renvoie les contours filtrés.
def rectContour(contours):
    rectCon = []
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            approx = getCornerPoints(i)
            if len(approx) == 4:
                rectCon.append(i)
    # Les rectangles sont ensuite triés par aire décroissante.
    rectCon = sorted(rectCon, key=cv2.contourArea, reverse=True)
    return rectCon


# La fonction prend en entrée un contour
def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True)
    # ça donne une approximation du contour avec un polygone pour obtenir les points de coin du contour.
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True)
    # renvoie les points de coin.
    return approx


def splitBoxes(img, questions, choices):
    # ça découpe une image en une grille de boîtes correspondant aux réponses.
    # verticalement pour chaque question
    rows = np.vsplit(img, questions)
    boxes = []
    for r in rows:
        # puis horizontalement pour chaque choix
        cols = np.hsplit(r, choices)
        for box in cols:
            boxes.append(box)
    # renvoie une liste de boîtes.
    return boxes


def drawGrid(img, questions, choices):
    # affiche une grille pour séparer chaque boîte en dessinant des lignes
    secW = int(img.shape[1] / choices)
    secH = int(img.shape[0] / questions)

    for i in range(1, choices):
        pt1 = (secW * i, 0)
        pt2 = (secW * i, img.shape[0])
        cv2.line(img, pt1, pt2, (255, 255, 0), 2)

    for i in range(1, questions):
        pt1 = (0, secH * i)
        pt2 = (img.shape[1], secH * i)
        cv2.line(img, pt1, pt2, (255, 255, 0), 2)

    return img


def showAnswers(img, myIndex, grading, ans, questions, choices):
    secW = int(img.shape[1] / choices)
    secH = int(img.shape[0] / questions)
    min_radius = min(secW, secH) // 3

    for x in range(0, questions):
        myAns = myIndex[x]
        cX = (myAns * secW) + secW // 2
        cY = (x * secH) + secH // 2

        if grading[x] == 1:
            # SI LA RÉPONSE COURANTE EST LA BONNE
            myColor = (0, 255, 0)
            cv2.circle(img, (cX, cY), min_radius, myColor, cv2.FILLED)
        else:
            # AUTREMENT, ELLE SERA COLORÉE EN ROUGE
            myColor = (0, 0, 255)
            cv2.circle(img, (cX, cY), min_radius, myColor, cv2.FILLED)

            # RÉPONSE CORRECTE
            myColor = (0, 255, 0)
            correctAns = ans[x]
            cv2.circle(img, ((correctAns * secW) + secW // 2, (x * secH) + secH // 2),
                       20, myColor, cv2.FILLED)  # LE RAYON EST DE 20, PLUS PETIT QUE LE 50


def read_data():
    # Utilisation de barres de défilement pour sélectionner le nombre de questions et de choix.
    questions = st.slider("How many questions there are?", 1, 20, 10)
    choices = st.slider("How many choices there are?", 1, 5, 5)

    answers = []
    for q in range(1, questions + 1):
        st.header(f"Question N°{q}")
        # Utilisation d'un menu déroulant pour choisir la réponse correcte.
        answer_str = st.selectbox(f"Choose the right answer of the question N°{q}",
                                  [chr(ord('a') + i) for i in range(choices)])
        # Convertir la lettre en nombre (a=0, b=1, c=2, ...)
        answer = ord(answer_str) - ord('a')
        answers.append(answer)

    st.subheader("Select a source for MCQ processing")
    # Utilisation d'une radio pour choisir entre la webcam et l'importation d'une image.
    webCamFeed = st.radio("Use webcam ?", ["No", "Yes", ]) == "Yes"
    if webCamFeed:
        nameImage = None
    else:
        # Utilisation d'un widget de texte pour entrer le chemin de l'image.
        file = st.file_uploader("Choose an image")
        if file:
            nameImage = file.name
            # print(nameImage)

    # Bouton pour soumettre les options.
    if st.button("Submit"):
        # Vérifier si le chemin de l'image existe s'il est spécifié.
        if not webCamFeed and (nameImage is None or not os.path.exists(nameImage)):
            st.error(f"Error : This path '{nameImage}' doesn't exist. Please try again.")
        else:
            st.success("Reading data was done.")
            return questions, choices, answers, webCamFeed, nameImage
    else:
        return None

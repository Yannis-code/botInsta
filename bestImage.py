# -*-coding:UTF8 -*
#-------------------------
# TD Morphologie
#@author: cteuliere
#-------------------------

import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
import sys

###############################################################
# Fonction de seuillage d'une image :

def Median(I, D):
    imgFiltre = np.zeros(I.shape)
    for i in range(1, len(I)-int(D/2)):
        for j in range(1, len(I[i])-int(D/2)):
            imgFiltre[i][j] = MedianFiltre(I, D, i, j)
    return imgFiltre

def MedianFiltre(I, D, x, y):
    med = []
    m = int(D/2)
    for i in range(D):
        for j in range(D):
            med.append(I[x + i-m][y + j-m])
    med.sort()
    return med[int(len(med)/2)]

def soustractionIm(I1, I2):
    Isous = np.zeros(I1.shape)
    for i in range(len(I1)):
        for j in range(len(I1[i])):
            Isous[i, j] = abs(I1[i, j] - I2[i, j])
            
    return Isous

def seuillageHyst(I, seuilMax, seuilMin):
    Is = np.zeros(I.shape)
    for i in range(len(I)):
        for j in range(len(I[i])):
            if I[i,j] >= seuilMax:
                Is[i, j] = 255
    nbrModif = 1
    while nbrModif > 0:
        nbrModif = 0
        for i in range(1, len(I)-1):
            for j in range(1, len(I[i]-1)):
                if I[i,j] >= seuilMin and Is[i, j] != 255 and ([i+1, j] == 255 or I[i-1, j] == 255 or [i, j+1] == 255 or I[i, j-1] == 255):
                    Is[i, j] = 255
                    nbrModif +=1
    return Is
    
def nbrBlackPixel(I):
    count = 0
    for i in range(len(I)):
        for j in range(len(I[i])):
            if I[i,j] == 0:
                count += 1
    return count

def initImage(filename):
    print(filename)
    im = cv2.imread(filename) #Lecture d'une image avec OpenCV
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) # Conversion en niveaux de gris
    im = Median(im, 5)  #Debruitage
    return im

def getContour(im, element):
    erode1 = cv2.erode(im, element, iterations = 1)
    dilate1 = cv2.dilate(im, element, iterations = 1)
    image = soustractionIm(erode1, dilate1)
    image2 = seuillageHyst(image, 200, 100)
    Isous = cv2.morphologyEx(image2, cv2.MORPH_OPEN, element)
    Isous = cv2.morphologyEx(Isous, cv2.MORPH_CLOSE, element)
    return Isous

def bestImage(im1, im2, im3, im4):
    bestIm = im1
    number = 1
    if nbrBlackPixel(bestIm) < nbrBlackPixel(im2):
        bestIm = im2
        number = 2
    if nbrBlackPixel(bestIm) < nbrBlackPixel(im3):
        bestIm = im3
        number = 3
    if nbrBlackPixel(bestIm) < nbrBlackPixel(im4):
        bestIm = im4
        number = 4
    return number
###############################################################
# Fonction principale du script :
def main(name = "ZoRfAzQpDIZaD-QGoXTyDg_"):
    
    #------------------------
    # Chargement de l'image
    #------------------------
    im1Couleur = cv2.imread("Image/2017_" + name + "0.jpg")
    im2Couleur = cv2.imread("Image/2017_" + name + "90.jpg")
    im3Couleur = cv2.imread("Image/2017_" + name + "180.jpg")
    im4Couleur = cv2.imread("Image/2017_" + name + "270.jpg")
    im1 = initImage("Image/2017_" + name + "0.jpg") #Lecture d'une image avec OpenCV
    im2 = initImage("Image/2017_" + name + "90.jpg")
    im3 = initImage("Image/2017_" + name + "180.jpg")
    im4 = initImage("Image/2017_" + name + "270.jpg")
    #---------------------------
    # Contoure
    #---------------------------
    element = np.ones((5,5),np.uint8)
    im1Modif = getContour(im1, element)
    im2Modif = getContour(im2, element)
    im3Modif = getContour(im3, element)
    im4Modif = getContour(im4, element)
    #opening= cv2.morphologyEx(closing, cv2.MORPH_OPEN, element)
    #closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, element)
    #-------------------------
    # Affichage du résultat : 
    #-------------------------

    number = bestImage(im1Modif, im2Modif, im3Modif, im4Modif)

    if number == 1:
        return "0.jpg"
    elif number == 2:
        return "90.jpg"
    elif number == 3:
        return "180.jpg"
    elif number == 4:
        return "270.jpg"

    return "Error"
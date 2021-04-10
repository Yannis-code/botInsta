##########################
##Code made by xerneas02##
##########################
import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
import sys

####################################################
## Denoising function by median of a color image: ##
####################################################
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


############################################################################
## Function which subtracts from each other all the pixels of two images: ##
############################################################################
def soustractionIm(I1, I2):
    Isous = np.zeros(I1.shape)
    for i in range(len(I1)):
        for j in range(len(I1[i])):
            Isous[i, j] = abs(I1[i, j] - I2[i, j])
            
    return Isous

###################################################
## Thresholding function to have a binary image: ##
###################################################

def seuillageHyst(I, seuilMax, seuilMin):
    """
    This function make thresholding by having thresholding sure and one unsure
    the function convert all the pixel with a higher value than the thresholding sure
    into white pixel and next all the pixels unsure that tuch a pixel sure into are also
    convert into white pixel. (the other pixels are black)
    """
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

###################################################################
## Function to get the number of black pixels in a binary image: ##
###################################################################
def nbrBlackPixel(I):
    count = 0
    for i in range(len(I)):
        for j in range(len(I[i])):
            if I[i,j] == 0:
                count += 1
    return count


####################################
## Function to initialize images: ##
####################################
def initImage(filename):
    """
    This function get an image from the path given, convert this image in black and white
    and apply a medina filtre to be sure that the image isn't noisy
    """
    print(filename)
    im = cv2.imread(filename)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im = Median(im, 5) 
    return im

################################################
## Function to have the outlines in an image: ##
################################################
def getContour(im, element):
    """
    This function return the soustraction of the erodation and dilation of the image
    and that give us an outline of th image.
    This outline is convert in a binary image.
    """
    erode1 = cv2.erode(im, element, iterations = 1)
    dilate1 = cv2.dilate(im, element, iterations = 1)
    image = soustractionIm(erode1, dilate1)
    image2 = seuillageHyst(image, 200, 100)
    Isous = cv2.morphologyEx(image2, cv2.MORPH_OPEN, element)
    Isous = cv2.morphologyEx(Isous, cv2.MORPH_CLOSE, element)
    return Isous

#######################################################
## Function to get the "best image" out of 4 images: ##
#######################################################
def bestImage(im1, im2, im3, im4):
    """
    This function get the best image out of 4 images by watching wich of this for images
    have the most black pixels in there outlines.
    It's the way i chose to know wich image have the most things to see in it.
    """
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

###################################
### Main function of the script: ##
###################################
def main(name = "ZoRfAzQpDIZaD-QGoXTyDg_"):
    """
    This function get the name of the picture in entry take the 4 pictures with that name in the folder Image
    and return wich one is the "best" image.
    """
    #------------------------
    # Image Loading
    #------------------------
    
    ## Get the color images
    im1Couleur = cv2.imread("Image/2017_" + name + "0.jpg")
    im2Couleur = cv2.imread("Image/2017_" + name + "90.jpg")
    im3Couleur = cv2.imread("Image/2017_" + name + "180.jpg")
    im4Couleur = cv2.imread("Image/2017_" + name + "270.jpg")
    
    ## Get the black ans white images
    im1 = initImage("Image/2017_" + name + "0.jpg") 
    im2 = initImage("Image/2017_" + name + "90.jpg")
    im3 = initImage("Image/2017_" + name + "180.jpg")
    im4 = initImage("Image/2017_" + name + "270.jpg")
    
    #---------------------------
    # Outlines Images
    #---------------------------
    
    element = np.ones((5,5),np.uint8)
    im1Modif = getContour(im1, element)
    im2Modif = getContour(im2, element)
    im3Modif = getContour(im3, element)
    im4Modif = getContour(im4, element)
    
    #-------------------------
    # Search the best image
    #-------------------------

    number = bestImage(im1Modif, im2Modif, im3Modif, im4Modif)
    
    #--------------------------
    # Return wich image to post
    #--------------------------
    
    # this just return th end of the name beacause it's the only thing that chages betewen the name of the different images
    if number == 1:
        return "0.jpg"
    elif number == 2:
        return "90.jpg"
    elif number == 3:
        return "180.jpg"
    elif number == 4:
        return "270.jpg"

    return "Error"

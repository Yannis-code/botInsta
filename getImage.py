import googleStreet.streetview as streetview
import bestImage
import matplotlib.pyplot as plt
import random
import geopy
from geopy.geocoders import Nominatim
import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys
from PIL import Image, ImageGrab
import os
import glob
import tiny_planet as tiny

def start():
    key = "AIzaSyCy4hb3E5eaX0bv1Qd46lQ5htSl85EaISs"
    dirc = "Image"
    lat = random.randint(-9000000,9000000)/100000
    lon = random.randint(-18000000,18000000)/100000
    panoids, lat, lon = streetview.panoids(lat=lat, lon=lon)
    #panoids, lat, lon = streetview.panoids(lat=36.1664594, lon=-115.1373683)   
    panoid = panoids[0]['panoid']
    locator = Nominatim(user_agent="myGeocoder")
    location = str(locator.reverse("{}, {}".format(lat, lon))).split(" ")
    country = location[len(location)-1]
    streetview.download_flats(panoid, key=key, flat_dir=dirc, fov=90, width=1080, height=1090)

    panorama = streetview.download_panorama_v3(panoid, zoom=3, disp=False)
    tiny.input_shape = panorama.shape
    final_image = tiny.warp(panorama, tiny.little_planet_3, output_shape=tiny.output_shape)
#    currentDT = datetime.datetime.now()
#    file_name = f"imgs/{currentDT.day}D{currentDT.month}M{currentDT.year}Y_{currentDT.hour}h{currentDT.minute}m{currentDT.second}s.jpg"
    file_name = "Image/Panorama.jpg"

    final_image = Image.fromarray((final_image * 255).round().astype(np.uint8), 'RGB')
    final_image.save(file_name)


    path = streetview.tiles_info(panoid)[0][2]
    path = path[:len(path)-7]

    path += bestImage.main(path)
    path = "Image/2017_" + path

    img = Image.open(path)
    area = (11, 0, 629, 618)
    cropped_img = img.crop(area)
    cropped_img.save("Image/imageToPost.jpg")
    return int(lat*100000)/100000, int(lon*100000)/100000, country
import streetview
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
    # Your Google Stret view API key here
    key = your_API_key
    dirc = "Image"
    # Getting the closest panorama ID of random lat/lon
    lat = random.randint(-9000000,9000000)/100000
    lon = random.randint(-18000000,18000000)/100000
    panoids, lat, lon = streetview.panoids(lat=lat, lon=lon) 
    panoid = panoids[0]['panoid']
    
    # Getting Country of the panorama 
    locator = Nominatim(user_agent="myGeocoder")
    location = str(locator.reverse("{}, {}".format(lat, lon))).split(" ")
    country = location[len(location)-1]
    
    # Download of 4 tiles of the panorama
    streetview.download_flats(panoid, key=key, flat_dir=dirc, fov=90, width=1080, height=1090)

    # Download of the panorama "photosphere"
    panorama = streetview.download_panorama_v3(panoid, zoom=3, disp=False)
    
    # Transforming the "photosphere" into a "tiny planet" and exporting it
    tiny.input_shape = panorama.shape
    final_image = tiny.warp(panorama, tiny.little_planet_3, output_shape=tiny.output_shape)
    file_name = "Image/Panorama.jpg"
    final_image = Image.fromarray((final_image * 255).round().astype(np.uint8), 'RGB')
    final_image.save(file_name)

    # Determining which of the 4 tiles has the most information
    path = streetview.tiles_info(panoid)[0][2]
    path = path[:len(path)-7]
    path += bestImage.main(path)
    path = "Image/2017_" + path

    # Cropping of the exported tile to get rid of google tags and exporting it
    img = Image.open(path)
    area = (11, 0, 629, 618)
    cropped_img = img.crop(area)
    cropped_img.save("Image/imageToPost.jpg")
    return int(lat*100000)/100000, int(lon*100000)/100000, country

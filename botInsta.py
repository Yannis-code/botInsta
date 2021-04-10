import os
import glob
from time import sleep
import random
from PIL import Image, ImageGrab
import getImage
from instagrapi import Client
from instagrapi.types import Location, Usertag

files = glob.glob('Image/*')
for f in files:
    os.remove(f)

lat, lon, country = getImage.start()


bot = Client()
bot.login("imageduglobe", "InstaBotTotorat")



yannis_id = bot.user_info(1722473835)
mathis_id = bot.user_info(19801251168)
tag = [Usertag(user=yannis_id, x=0, y=1), Usertag(user=mathis_id, x=1, y=1)]


album_path = ["Image/Panorama.jpg", "Image/imageToPost.jpg"]
text =  "Pays : " + str(country) + "\nLatitude : {}, Longitude : {}".format(lat, lon) + "\nImage from google map posted by my bot.\nBot made by @eikthyrnir02 and @yannis.rch\n#googlemap #googleearth #googlestreetview #google #bot #photo #paysage #picture #landscape #beautifull #programmation #code #programming #globe #earth #panorama #360 #litleplanet #tinyplanet #ia #random"
loc = bot.location_complete(Location(name=country, lat=lat, lng=lon))
id = str(bot.album_upload(
    album_path,
    caption = text,
    location = loc,
    usertags=tag
)).split(" ")[1]
id = id[4:len(id)-1]
print (id)
print("Images published!")

#bot.media_like(id)
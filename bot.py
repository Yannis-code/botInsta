import os
import glob
from time import sleep
import random
from PIL import Image, ImageGrab
import getImage
from instagrapi import Client
from instagrapi.types import Location, Usertag

# Removing of the previous post if it is not already done
files = glob.glob('Image/*')
for f in files:
    os.remove(f)

# Gathering some information about the images
lat, lon, country = getImage.start()

USERNAME = account_username
PASSWORD = acount_password

# Creating a bot from instagrapi and login in into the instagram account
bot = Client()
bot.login(USERNAME, PASSWORD)

"""
    Getting informations about 2 users with their Instagram user Id
    Instagram user Id can be get by running "print(bot.user_info_by_username(username))"
    User id is a integer: "123456789"
"""
usr1_id = bot.user_info(XXXXXXXXXXX)
usr2_id = bot.user_info(XXXXXXXXXXX)

# Create Usertag objet to pin on the post
tag = [Usertag(user=usr1_id, x=0, y=1), Usertag(user=usr2_id, x=1, y=1)]

# List of Path to images to post
album_path = ["Image/Panorama.jpg", "Image/imageToPost.jpg"]

# Caption of the post
text =  "Pays : " + str(country) + "\nLatitude : {}, Longitude : {}".format(lat, lon) + \
"\nImage from google map posted by my bot.\nBot made by @usr1 and @usr1\n#googlemap #googleearth #googlestreetview "\
"#google #bot #photo #paysage #picture #landscape #beautifull #programmation #code #programming #globe #earth #panorama #360 "\
"#litleplanet #tinyplanet #ia #random"

# Creating of the location of the pictures
loc = bot.location_complete(Location(name=country, lat=lat, lng=lon))

# Uploading the album to Instagram
bot.album_upload(album_path, caption = text, location = loc, usertags=tag)
print("Images published!")

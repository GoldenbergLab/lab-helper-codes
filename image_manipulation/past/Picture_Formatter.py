from PIL import Image, ImageOps
import os
import re
import cv2
import os
import numpy as np
### READ ME

#Generally
# This code has 4 main functions which can be applied to a single image or a whole directory of images
# name changer: takes a picture and changes the number index of the picture according to the rule, which is right now, if a picture is for e.g. A01 it will add 50 to it to make it A51.
# you can change the roles for labeling according to your needs
# size changer: takes an image and changes the size proportionally. Right now it creates images of the widht 141pixels
# background_color_changer: takes a picture and changes the background to grey
# remover: removes files from directory
# LOOPS AT THE BOTTOM: They can be used to process a whole batch/directory
# LOOP 1: changes all names by creating a copy with the new name. It also removes the old version with the old name
# LOOP 2: changes the background and the size of all files


# For tasks related to image Morphs
# This code transforms the original morphs that you get from fantamorph into the right SIZE, LABEL, and BACKGROUND
# In case that some pictures are to bright change the variables such as sensitiyity in the function background_color_changer
# Mind that the input picture size has to be around 500 * 650
# otherwise you have to adjust the x, y, w, h = 140, 100, 200, 550 values in background_color_changer
# I will change that requirement at some point :D

# listing all files
current_path = os.getcwd()
file_location = os.path.join(current_path)  # exact location of basefile

def name_changer(file):
	image_name = file
	number_of_image = int(re.sub('[^0-9a]+', '', image_name))
	letter_of_image = image_name[0]
	if number_of_image < 51:
		number_of_image += 50
	img_name_jpg = letter_of_image + str(number_of_image) + ".jpg"
	return img_name_jpg


def size_changer(file):
	basewidth = 141 # in pixel
	img = Image.open(file)
	wpercent = (basewidth / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((basewidth, hsize), Image.ANTIALIAS)
	img.save(file)

def background_color_changer(file):
	# Read image
	image = cv2.imread(file)

	# Convert to HSV
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	# Define lower and uppper limits of what we call "white-ish"
	sensitivity = 70
	lower_white = np.array([0, 0, 255 - sensitivity])
	upper_white = np.array([255, sensitivity, 255])

	# Create mask to only select white
	mask = cv2.inRange(hsv, lower_white, upper_white)

	# Draw new rectangular mask on old mask that is black inside the rectangle and white outside the rectangle
	x, y, w, h = 140, 100, 200, 550
	mask2 = mask.copy()
	cv2.rectangle(mask2, (x, y), (x + w, y + h), 0, -1)

	# Change image to grey where we found white for combined mask
	result = image.copy()
	result[mask2 > 0] = (170, 170, 170)

	# save results
	cv2.imwrite(file, result)

def remover (files):
	image_name = file
	number_of_image = int(re.sub('[^0-9a]+', '', image_name))
	letter_of_image = image_name[0]
	if number_of_image < 51:
		os.remove(file)

# LOOP 1
for file in os.listdir(file_location): #This loop changes all names by creating a copy with the new name. It also removes the old version with the old name
	if file.endswith(".jpg"):
		name = name_changer(file)
		ImageOps.expand(Image.open(file)).save(name)
		remover(file)

# LOOP 2
for file in os.listdir(file_location): #this loop changes the background and the size of all files
	if file.endswith(".jpg"):
		background_color_changer(file)
		size_changer(file)



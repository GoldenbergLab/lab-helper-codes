from PIL import Image, ImageOps
import os
import re
import cv2
import os
import numpy as np


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
	basewidth = 141
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

for file in os.listdir(file_location):
	if file.endswith(".jpg"):
		name = name_changer(file)
		ImageOps.expand(Image.open(file)).save(name)
		remover(file)

for file in os.listdir(file_location):
	if file.endswith(".jpg"):
		name = name_changer(file)
		remover(file)
		background_color_changer(file)
		size_changer(file)



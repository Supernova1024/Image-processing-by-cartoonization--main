import sys
import getopt
import time
import cv2

import centralize
import background_removal
import cartoonize
import secrets

def put_text_at_angle(image, str_key):

	font = cv2.FONT_HERSHEY_SIMPLEX
	textX = 10
	textY = 30
	textY_max = image.shape[0]
	for char in str_key:
		if textY > textY_max - 20:
			break;
		cv2.putText(image, char, (textX, textY ), font, 1, (0, 0, 0), 3)
		textY += 30
	textX = int(image.shape[1] - 40)
	textY = 30
	for char in str_key:
		if textY > textY_max - 20:
			break;
		cv2.putText(image, char, (textX, textY ), font, 1, (0, 0, 0), 3)
		textY += 30
	return image

def main(argv):

	inputfile = ''
	backgroundfile = ''
	person_name = ''
	serial_key = ''
	background_folder = 'image_processing/background'
	carton_folder = 'image_processing/cartoonized_images'
	back_removal_folder = 'image_processing/background_removal_images'
	output_path = 'image_processing/final_result'
	ratio = 1.0

	try:
		opts, args = getopt.getopt(argv,"hi:b:n:k:",["ifile=","bfile=", "name=", "key="])
	except getopt.GetoptError:
		print ('main.py -i <inputfile> -b <backgroundfile> -b <person_name> -k <serial_key>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('main.py -i <inputfile> -o <backgroundfile> -b <person_name>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-b", "--bfile"):
			backgroundfile = arg
		elif opt in ("-n", "--name"):
			person_name = arg
		elif opt in ("-k", "--key"):
			serial_key = arg
	# print ('Input file is ', inputfile)
	# print ('Background file is ', backgroundfile)
	# print ('Person name is ', person_name)

	# Cartoonize the image
	# print ("***** Step 1: Cartoonization *****")
	real_input_file = inputfile.split('/')[4] + '_' + inputfile.split('/')[5]
	carto_image = cartoonize.run(inputfile, carton_folder + '/' + real_input_file)

	# # Background Removal
	# print ("***** Step 2: Background Removal *****")
	background_removal_url = background_removal.run(carto_image)
	time.sleep(5)

	# background_removal_url = 'https://res.cloudinary.com/ds8bfj14k/image/upload/v1615793499/ogdg4oiyuzlgmxgqveky.png'
	# background_removal_url = 'https://res.cloudinary.com/dtvs6wlp0/image/upload/v1615870636/zdbywrnc1hsmohpzlomt.png'

	# Centralize the image to the background
	# print ("***** Step 3: Centralization *****")
	final_path = output_path + '/' + inputfile
	centralized_img = centralize.run(background_removal_url, background_folder + '/' + backgroundfile, final_path, ratio)


	# Making Border of the image and put Name at the bottom and center of image
	# print ("***** Step 4: Put Name at the bottom and center *****")
	borderType = cv2.BORDER_CONSTANT
	
	margin = int(0.05 * centralized_img.shape[0])  # shape[0] = rows
	
	img = cv2.copyMakeBorder(centralized_img, margin, margin, margin, margin, borderType, None, [255, 255, 255])

	# Center text on an image
	font = cv2.FONT_HERSHEY_SIMPLEX
	# get boundary of this text
	textsize = cv2.getTextSize(person_name, font, 1, 2)[0]

	# get coords based on boundary
	textX = int((img.shape[1] - textsize[0]) / 2)
	textY = int(img.shape[0] - textsize[1])

	# add text centered on image
	cv2.putText(img, person_name, (textX, textY ), font, 1, (0, 0, 0), 3)

	# add
	image = put_text_at_angle(img, serial_key)
	# cv2.imshow('image', img)
	output_file = output_path + '/user_' + secrets.token_hex(nbytes=16) + '.png'
	cv2.imwrite(output_file, image)
	cv2.waitKey(0)
	print (output_file)

if __name__ == '__main__':
	main(sys.argv[1:])
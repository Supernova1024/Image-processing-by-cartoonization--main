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
	person_name = ''
	serial_key = ''
	output_path = 'image_processing/final_result'

	try:
		opts, args = getopt.getopt(argv,"hi:n:k:",["ifile=","name=", "key="])
	except getopt.GetoptError:
		print ('main.py -i <inputfile> -n <person_name> -k <serial_key>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('naming.py -i <inputfile> -n <person_name> -k <serial_key>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-n", "--name"):
			person_name = arg
		elif opt in ("-k", "--key"):
			serial_key = arg

	img = cv2.imread(inputfile, cv2.IMREAD_UNCHANGED)

	# Center text on an image
	font = cv2.FONT_HERSHEY_SIMPLEX

	# get boundary of this text
	textsize = cv2.getTextSize(person_name, font, 1, 2)[0]

	# get coords based on boundary
	textX = int((img.shape[1] - textsize[0]) / 2)
	textY = int(img.shape[0] - textsize[1] * 2)

	# add text centered on image
	cv2.putText(img, person_name, (textX, textY), font, 1, (255, 255, 255), 3)

	# add
	image = put_text_at_angle(img, serial_key)
	# cv2.imshow('image', img)
	output_file = output_path + '/user_' + secrets.token_hex(nbytes=16) + '.png'
	cv2.imwrite(output_file, image)
	cv2.waitKey(0)
	print (output_file)

if __name__ == '__main__':
	main(sys.argv[1:])
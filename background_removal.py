import cloudinary
from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import urllib.request

def dump_response(response):
	print("Upload response:")
	for key in sorted(response.keys()):
		print("  %s: %s" % (key, response[key]))


def run(file):
	# cloudinary.config( 
	# 	cloud_name = "ds8bfj14k", 
	# 	api_key = "557428955162675", 
	# 	api_secret = "I1H03hfUGl4EK3p8PPnPomUQKv8"
	# )

	cloudinary.config( 
		cloud_name = "dtvs6wlp0", 
		api_key = "654975852319676", 
		api_secret = "uPEjKxmeBDldZsnd6ytTS2OfRks"
	)

	response = upload(file, background_removal = "cloudinary_ai:fine_edges")
	# dump_response(response)

	url, options = cloudinary_url(
		response['public_id'],
		format=response['format'],
	)
	updated_url = url[:-3] + 'png'
	return updated_url

if __name__ == '__main__':
	file = "cartoonized_images/party5.jpg"
	destination_path = 'background_removal_images/party5.jpg'
	run(file)

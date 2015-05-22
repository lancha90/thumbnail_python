import Image, os, sys, errno
import urllib
import time
from pymongo import MongoClient
from flask import Flask
from flask import send_file
from image import Thumbnails

app = Flask(__name__)

IN_DIR = 'input/'
OUT_DIR = 'output/'
SIZE = 300,300

client = MongoClient('127.0.0.1', 27017)
db = client['adk_thumbnails']



def thumbnail(_id,_url):
	filename = "%s%s_original.jpeg" % (IN_DIR, _id)
	download_file = urllib.URLopener()
	download_file.retrieve(_url, filename)
	
	img = Image.open(filename)
	img.thumbnail(SIZE, Image.ANTIALIAS)
	to_save_name = '%sthumbnail_%s.jpeg' % (OUT_DIR,_id)
	img.save( to_save_name, "JPEG")

	print '----> 1'
	to_insert = Thumbnails(db)
	print '----> 2'
	to_insert.img_id = _id
	to_insert.img_path = to_save_name
	to_insert.img_url = _url
	to_insert.timestamp = time.strftime("%Y/%m/%d %H:%M:%S")
	print to_insert.to_JSON()

	try:
		os.remove(filename)
	except OSError:
		pass

	return to_save_name

def urlFile(_id):
	filename = '%sthumbnail_%s.jpeg' % (OUT_DIR,_id)
	if os.path.exists(filename):
		return filename

	return None

# =========== ROUTES ================

@app.route("/")
def hello():
	return "Server is running......"

@app.route("/image/<_id>/<path:_url>")
def image(_id,_url):

	filename = urlFile(_id)
	
	if filename is None:
		filename = thumbnail(_id,_url)

	return send_file(filename, mimetype='image/jpeg')

if __name__ == "__main__":
	app.run()
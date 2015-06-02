from pymongo.son_manipulator import SONManipulator
class Thumbnails (object):


	img_path = ''
	last_download = ''

	def toJSON(_self):
		return {"path": _self.img_path,"last_download":_self.last_download}
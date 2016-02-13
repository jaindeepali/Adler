import os
import json

import requests
import zipfile

class Base(object):

	def __init__(self):
		dir = os.path.dirname(__file__)
		# Read config
		self.config_file_path = os.path.join(dir, 'config', 'config.json')
		with open(self.config_file_path, 'r') as config_file:
			config = json.loads(config_file.read())
		
		# Data paths
		self.data_path = os.path.join(config['data_dir'], 'data')
		self.data_url = config['data_url']
		self.category_listing_url = config['category_listing_url']
		self.raw_data_path = os.path.join(
			self.data_path, 'raw_data')
		self.data_object_path = os.path.join(self.data_path, 'data_objects')
		self.samples_path = os.path.join(
			self.data_path, 'data_objects', 'samples')
		self.category_listing_document_path = os.path.join(
			self.data_path, 'category_list.html')

		# Create data paths
		self._mkdir_p(self.samples_path)
		self._mkdir_p(self.raw_data_path)

	def fetch_data(self):
		print "Downloading data..."
		temp_zip = os.path.join(self.data_path, 'temp.zip')
		try:
			response = requests.get(self.data_url)
		except IOError, e:
			print "Can't retrieve %r to %r: %s" % (
				self.data_url, self.data_path, e)
			return
		with open(temp_zip, 'wb') as f:
			f.write(response.content)

		try:
			z = zipfile.ZipFile(temp_zip, 'r')
		except zipfile.error, e:
			print "Bad zipfile (from %r): %s" % (self.data_url, e)
			return
		z.extractall(path=self.raw_data_path)
		print "Data downloaded and unzipped"

		print "Downloading category listing..."
		try:
			response = requests.get(self.category_listing_url)
		except IOError, e:
			print "Can't retrieve %r to %r: %s" % (
				self.data_url, self.data_path, e)
			return
		with open(self.category_listing_document_path, 'wb') as f:
			f.write(response.content)
		print "Category listing downloaded"

	def _mkdir_p(self, path):
		try:
			os.makedirs(path)
		except OSError:
			if os.path.isdir(path):
				pass
			else: raise

if __name__ == '__main__':
	ob = Base()
	ob.fetch_data()
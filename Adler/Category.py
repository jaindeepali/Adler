import os
import pickle

from bs4 import BeautifulSoup as BS

from Base import Base


class Category(Base):

	def __init__(self):
		Base.__init__(self)
		self.listing_data_object_path = os.path.join(
			self.data_object_path, 'category_list.p')
		self.category_list = {}

	def from_id(self, id):
		if not self.category_list:
			if os.path.exists(self.listing_data_object_path):
				self.category_list = pickle.load(
					open(self.listing_data_object_path))
			else:
				self.save_list()
		return self.category_list[id]

	def get_list(self):
		listing_document = BS(open(self.category_listing_document_path, 'r').read())
		for row in listing_document.select('tr'):
			for category_element in row.select('a'):
				category_url = category_element['href']
				category_id = category_element.text
				category_text = category_url.split('.org/')[1]
				self.category_list[category_id] = category_text

	def save_list(self):
		self.get_list()
		pickle.dump(self.category_list, open(
			self.listing_data_object_path, 'wb'))

if __name__ == '__main__':
	ob = Category()
	print ob.from_id('5560')
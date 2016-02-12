from bs4 import BeautifulSoup as BS
import pickle
import os

class Category():

	def __init__(self):
		self.listing_document_path = os.path.join('data', 'Tech300Categories.html')
		self.listing_data_object_path = os.path.join('data_objects', 'category_list.p')
		self.listing_document = BS( open(self.listing_document_path, 'r').read() )
		self.category_list = {}

	def from_id(self, id):
		if os.path.exists(self.listing_data_object_path):
			self.category_list = pickle.load(open(self.listing_data_object_path))
		else:
			self.get_list()
		return self.category_list[id]

	def get_list(self):
		for row in self.listing_document.select('tr'):
			for category_element in row.select('a'):
				category_url = category_element['href']
				category_id = category_element.text
				category_text = category_url.split('.org/')[1]
				self.category_list[category_id] = category_text
		return

	def save_list(self):
		self.get_list()
		pickle.dump(self.category_list, open(self.listing_data_object_path, 'wb'))
		return

if __name__ == '__main__':
	ob = Category()
	ob.save_list()
	print ob.from_id('5560') 
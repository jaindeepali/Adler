from bs4 import BeautifulSoup as BS
import pickle
import os

class Category():

	def __init__(self):
		self.listing_document_path = os.path.join('data', 'Tech100Categories.html')
		self.listing_document = BS( open(self.listing_document_path, 'r').read() )

	def from_id(self, id):
		return

	def get_list(self):
		self.category_list = {}
		i = 0
		for row in self.listing_document.select('tr'):
			for category_element in row.select('a'):
				i = i + 1
				category_url = category_element['href']
				category_id = category_element.text
				print i, category_id, category_url
		return

	def save_list(self):
		return

if __name__ == '__main__':
	ob = Category()
	ob.get_list() 
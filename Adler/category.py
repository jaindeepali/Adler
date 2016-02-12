from bs4 import BeautifulSoup as BS
import pickle
import os

class Category():

	def __init__(self):
		dir = os.path.dirname(__file__)
		self.listing_document_path = os.path.join(dir, 'data', 'Tech300Categories.html')
		self.listing_data_object_path = os.path.join(dir, 'data_objects', 'category_list.p')
		self.category_list = {}

	def fromId(self, id):
		if len(self.category_list) == 0:
			if os.path.exists(self.listing_data_object_path):
				self.category_list = pickle.load(open(self.listing_data_object_path))
			else:
				self.saveList()
		return self.category_list[id]

	def getList(self):
		listing_document = BS( open(self.listing_document_path, 'r').read() )
		for row in listing_document.select('tr'):
			for category_element in row.select('a'):
				category_url = category_element['href']
				category_id = category_element.text
				category_text = category_url.split('.org/')[1]
				self.category_list[category_id] = category_text
		return

	def saveList(self):
		self.getList()
		pickle.dump(self.category_list, open(self.listing_data_object_path, 'wb'))
		return

if __name__ == '__main__':
	ob = Category()
	ob.saveList()
	print ob.fromId('5560') 
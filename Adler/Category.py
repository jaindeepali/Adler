import os
import pickle

from bs4 import BeautifulSoup as BS

from Base import Base

CATEGORIES = {
	'Business_and_Economy': ['Business_and_Economy'],
	'Computers': ['Computers'],
	'Sports': ['Sports', 'Football', 'Golf'],
	'Society_and_Culture': ['Society_and_Culture', 'Society', 'Religion', 'Ethnicity', 'Philosophy', 'Home'],
	'Recreation': ['Recreation', 'Games', 'Travel_and_Tourism'],
	'Vehicles': ['Vehicles'],
	'Education': ['Education'],
	'Politics': ['Politics', 'Government'],
	'Arts_and_Entertainment': ['Arts_and_Entertainment', 'Arts', 'Music', 'Crafts'],
	'Health': ['Health', ],
	'Electronics_and_Electrical': ['Electronics_and_Electrical'],
	'News': ['News'],
	'Science': ['Science'],
	'Publications': ['Publications'],
	'Business': ['Business']
}

class Category(Base):

	def __init__(self):
		Base.__init__(self)
		
		self.listing_data_object_path = os.path.join(
			self.data_object_path, 'category_list.p')
		self.category_done_list_object_path = os.path.join(
			self.data_path, 'category_done_list.p')

		self.category_list = {}
		self.category_done_list = []

	def from_id(self, id):
		if not self.category_list:
			if os.path.exists(self.listing_data_object_path):
				self.category_list = pickle.load(
					open(self.listing_data_object_path))
			else:
				self.save_list()
		
		return self.category_list[id]

	def _get_category(self, text):
		category = ''

		probable_categories = text.split('/')
		
		for pcat in reversed(probable_categories):
			for cat in CATEGORIES:
				if pcat in CATEGORIES[cat]:
					category = cat
		if not category:
			category = 'NA'
		
		if category == 'Business':
			category = probable_categories[1]

		return category

	def get_list(self):
		listing_document = BS(open(
			self.category_listing_document_path, 'r').read())
		
		for row in listing_document.select('tr'):
			for category_element in row.select('a'):
				category_url = category_element['href']
				category_id = category_element.text
				category_text = category_url.split('.org/')[1]
				category = self._get_category(category_text)
				self.category_list[category_id] = category

	def save_list(self):
		self.get_list()

		pickle.dump(self.category_list, open(
			self.listing_data_object_path, 'wb'))

	def get_category_done_list(self):
		if os.path.exists(self.category_done_list_object_path):
			self.category_done_list = pickle.load(open(
				self.category_done_list_object_path, 'r'))

	def update_category_done_list(self, clist):
		self.category_done_list.extend(clist)
		pickle.dump(self.category_done_list, open(
			self.category_done_list_object_path, 'wb'))

	def destroy_category_done_list(self):
		if os.path.exists(self.category_done_list_object_path):
			os.remove(self.category_done_list_object_path)

if __name__ == '__main__':
	ob = Category()
	ob.save_list()
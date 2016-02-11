import pickle
import os
from feature import Feature
from category import Category

class Document():

	def __init__(self, exp):
		self.exp = exp

	def get_category(self, id):
		return

	def get_feature_list(self, id):
		return

	def parse_all_docs(self):
		return

	def save_feature_vector(self):
		return

if __name__ == '__main__':
	ob = Document('Exp_1622_42350')
	ob.save_list() 
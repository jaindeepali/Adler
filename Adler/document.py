import pandas
import pickle
import os
from feature import Feature
from category import Category

class Document():

	def __init__(self, exp):
		self.exp = exp
		self.listing_document_path = os.path.join('data', 'techtc300_preprocessed', exp, 'vectors.dat')
		self.listing_data_object_path = os.path.join('data_objects', self.exp + '_training_data.p')
		self.feature_list = []
		self.get_categories()

	def get_categories(self):
		_ , cat1, cat2 = self.exp.split('_')
		ob = Category()
		self.category1 = ob.from_id(cat1)
		self.category2 = ob.from_id(cat2)
		return

	def _get_features(self, flist):
		feature_list = {}
		ob = Feature(self.exp)
		for l in flist:
			fid, freq = l.split(':')
			feature = ob.from_id(int(fid) - 1)
			feature_list[feature] = freq
		return feature_list

	def _get_training_sample(self, category, features):
		if category == '+1':
			features['Category'] = self.category1
		else:
			features['Category'] = self.category2
		return features

	def parse_all_docs(self):
		with open(self.listing_document_path, 'r') as f:
			lines = [line.strip() for line in f]
			lines = [line for line in lines if (line and line[0] != '#')]
			for document in lines:
				elements = document.split(' ')
				category = elements[0]
				features = self._get_features(elements[1:])
				sample = self._get_training_sample(category, features)
		return

	def save_training_data(self):
		return

if __name__ == '__main__':
	ob = Document('Exp_1622_42350')
	ob.parse_all_docs() 
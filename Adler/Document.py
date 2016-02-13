import os
import re
import pickle

import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from Base import Base
from Feature import Feature
from Category import Category


class Document(Base):

	def __init__(self, exp):
		Base.__init__(self)
		self.exp = exp
		self.listing_document_path = os.path.join(
			self.raw_data_path, exp, 'vectors.dat')
		self.samples_data_object_path = os.path.join(
			self.samples_path, self.exp + '_samples.p')
		self.feature_list = []
		self.get_categories()
		self.stop = stopwords.words('english')
		self.stop.append('')
		self.stemmer = PorterStemmer()
		self.samples = pd.DataFrame()

	def get_categories(self):
		__, cat1, cat2 = self.exp.split('_')
		ob = Category()
		self.category1 = ob.from_id(cat1)
		self.category2 = ob.from_id(cat2)

	def _get_features(self, ob, flist):
		feature_list = {}
		for l in flist:
			fid, freq = l.split(':')
			feature = ob.from_id(int(fid) - 1)
			# Keep only digits
			feature = re.sub("[^a-zA-Z]", "", feature)
			# Remove stop words
			if feature not in self.stop:
				# Stemming reduces derivatives to the base word
				feature = self.stemmer.stem(feature)
				if feature in feature_list:
					feature_list[feature] += int(freq)
				else:
					feature_list[feature] = int(freq)
		return pd.DataFrame([feature_list])

	def _get_training_sample(self, category, features):
		if category == '+1':
			features['Category'] = self.category1
		else:
			features['Category'] = self.category2
		return features

	def parse_all_docs(self):
		ob = Feature(self.exp)
		print "Parsing document in " + self.exp
		with open(self.listing_document_path, 'r') as f:
			lines = [line.strip() for line in f]
			lines = [line for line in lines if (line and line[0] != '#')]
			
			for idx, document in enumerate(lines):
				elements = document.split(' ')
				category = elements[0]
				features = self._get_features(ob, elements[1:])
				sample = self._get_training_sample(category, features)
				self.samples = self.samples.append(sample, ignore_index=True)
				print "Document #" + str(idx + 1) + " parsed"
			self.samples = self.samples.fillna(0)
		ob.destroy_list()

	def save_samples(self):
		self.parse_all_docs()
		pickle.dump(self.samples, open(self.samples_data_object_path, 'wb'))

if __name__ == '__main__':
	ob = Document('Exp_1622_42350')
	ob.save_samples()

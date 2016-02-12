import pandas as pd
import pickle
import os
import re
from nltk.corpus import stopwords
from nltk.stem.porter import *
from feature import Feature
from category import Category

class Document():

	def __init__(self, exp):
		dir = os.path.dirname(__file__)
		self.exp = exp
		self.listing_document_path = os.path.join(dir, 'data', 'techtc300_preprocessed', exp, 'vectors.dat')
		self.samples_data_object_path = os.path.join(dir, 'data_objects', 'samples', self.exp + '_samples.p')
		self.feature_list = []
		self.getCategories()
		self.stop = stopwords.words('english')
		self.stop.append('')
		self.stemmer = PorterStemmer()
		self.samples = pd.DataFrame()

	def getCategories(self):
		_ , cat1, cat2 = self.exp.split('_')
		ob = Category()
		self.category1 = ob.fromId(cat1)
		self.category2 = ob.fromId(cat2)
		return

	def _getFeatures(self, flist):
		feature_list = {}
		ob = Feature(self.exp)
		for l in flist:
			fid, freq = l.split(':')
			feature = ob.fromId(int(fid) - 1)
			feature = re.sub("[^a-zA-Z]", "", feature)
			if feature not in self.stop:
				feature = self.stemmer.stem(feature)
				if feature in feature_list:
					feature_list[feature] += int(freq)
				else:
					feature_list[feature] = int(freq)
		return pd.DataFrame([feature_list])

	def _getTrainingSample(self, category, features):
		if category == '+1':
			features['Category'] = self.category1
		else:
			features['Category'] = self.category2
		return features

	def parseAllDocs(self):
		print "Parsing document in " + self.exp
		i = 1
		with open(self.listing_document_path, 'r') as f:
			lines = [line.strip() for line in f]
			lines = [line for line in lines if (line and line[0] != '#')]
			for document in lines:
				elements = document.split(' ')
				category = elements[0]
				features = self._getFeatures(elements[1:])
				sample = self._getTrainingSample(category, features)
				self.samples = self.samples.append(sample, ignore_index=True)
				print "Document #" + str(i) + " parsed"
				if i == 4:
					break
				i = i + 1
			self.samples = self.samples.fillna(0)
		return

	def saveSamples(self):
		self.parseAllDocs()
		pickle.dump(self.samples, open(self.samples_data_object_path, 'wb'))
		return

if __name__ == '__main__':
	ob = Document('Exp_1622_42350')
	ob.saveSamples()
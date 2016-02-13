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
		
		self.samples = pd.DataFrame()

		self.get_categories()

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
			stop = stopwords.words('english')
			stop.append('')
			
			if feature not in stop:
				
				# Stemming reduces derivatives to the base word
				stemmer = PorterStemmer()
				feature = stemmer.stem(feature)
				
				if feature in feature_list:
					feature_list[feature] += int(freq)
				else:
					feature_list[feature] = int(freq)
		
		return pd.DataFrame([feature_list])

	def _get_category(self, category):
		if category == '+1':
			return self.category1
		else:
			return self.category2

	def parse_all_docs(self):
		ob = Feature(self.exp)
		
		print "Parsing documents in " + self.exp
		
		with open(self.listing_document_path, 'r') as f:
			lines = [line.strip() for line in f]
			lines = [line for line in lines[2:] if line]
			
			document_id = ''
			for line in lines:
				elements = line.split(' ')
				if elements[0] == '#':
					document_id = elements[3]
					continue
				
				category = self._get_category(elements[0])
				if category == 'NA':
					continue
				
				sample = self._get_features(ob, elements[1:])
				sample['Category'] = category
				sample['Id'] = document_id

				self.samples = self.samples.append(sample, ignore_index=True)
				
				print "Document #" + document_id + " parsed"
			
			self.samples = self.samples.fillna(0)
		
		print "Documents in " + self.exp + ' parsed'

		ob.destroy_list()

	def save_samples(self):
		self.parse_all_docs()
		
		if len(self.samples) > 0:
			pickle.dump(self.samples, open(self.samples_data_object_path, 'wb'))

if __name__ == '__main__':
	ob = Document('Exp_1622_42350')
	ob.save_samples()

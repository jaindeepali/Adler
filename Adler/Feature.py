import os
import re
import pickle

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from Base import Base

class Feature(Base):

	def __init__(self, exp):
		Base.__init__(self)

		self.exp = exp
		
		self.listing_document_path = os.path.join(
			self.raw_data_path, exp, 'features.idx')
		self.listing_data_object_path = os.path.join(
			self.data_object_path, self.exp + '_feature_list.p')
		
		self.feature_list = []

	def from_id(self, id):
		if not self.feature_list:
			
			if os.path.exists(self.listing_data_object_path):
				self.feature_list = pickle.load(
					open(self.listing_data_object_path))
			else:
				self.save_list()
		
		return self.feature_list[id]

	def filter_feature(self, feature):
		# Reasonable word length range
		if len(feature) < 2 or len(feature) > 40:
			return ''

		# Keep only letters
		feature = re.sub("[^a-zA-Z]", "", feature)
		
		# Remove words with the same letter more than 2 times in a row
		if re.search(r"(.)\1{2,}", feature):
			return ''

		# Remove words with more than 7 consecutive consonants
		consonant_groups = re.findall('[bcdfghjklmnpqrstvwxz]+', feature)
		if consonant_groups:
			if max([len(w) for w in consonant_groups]) > 7:
				return ''

		# Remove stop words
		stop = stopwords.words('english')
		if feature in stop:
			return ''

		# Stemming reduces derivatives to the base word
		stemmer = PorterStemmer()
		feature = stemmer.stem(feature)

		return feature

	def get_list(self):
		with open(self.listing_document_path, 'r') as f:
			lines = [line.strip() for line in f]
			lines = [line for line in lines if (line and line[0] != '#')]
			self.feature_list = [l.split(' ')[1] for l in lines]

	def save_list(self):
		self.get_list()
		
		pickle.dump(self.feature_list, open(
			self.listing_data_object_path, 'wb'))

	def destroy_list(self):
		if os.path.exists(self.listing_data_object_path):
			os.remove(self.listing_data_object_path)

if __name__ == '__main__':
	ob = Feature('Exp_1622_42350')
	ob.save_list()
	print ob.from_id(23)

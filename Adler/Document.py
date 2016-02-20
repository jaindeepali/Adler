import os
import pickle
import time

import pandas as pd

from Base import Base
from Feature import Feature
from Category import Category


class Document(Base):

	def __init__(self, exp, ignore_duplicate_category=False):
		Base.__init__(self)
		
		self.exp = exp
		self.ignore_duplicate_category = ignore_duplicate_category
		
		self.listing_document_path = os.path.join(
			self.raw_data_path, exp, 'vectors.dat')
		self.samples_data_object_path = os.path.join(
			self.samples_path, self.exp + '_samples.p')
		
		self.samples = pd.DataFrame()

		self.get_categories()

	def get_categories(self):
		__, self.category_id1, self.category_id2 = self.exp.split('_')
		
		ob = Category()
		self.category1 = ob.from_id(self.category_id1)
		self.category2 = ob.from_id(self.category_id2)

	def _get_features(self, ob, flist):
		feature_list = {}
		
		for l in flist:
			fid, freq = l.split(':')
			feature = ob.from_id(int(fid) - 1)
			
			feature = ob.filter_feature(feature)
			if not feature:
				continue
			
			feature_list[feature] = feature_list.get(feature, 0) + int(freq)
		
		return pd.DataFrame([feature_list])

	def _get_category(self, category):
		if category == '+1':
			return (self.category_id1, self.category1)
		else:
			return (self.category_id2, self.category2)

	def parse_all_docs(self):
		fob = Feature(self.exp)
		
		cob = Category()
		cob.get_category_done_list()

		stime = time.time()
		print "Parsing documents in " + self.exp
		print "Start time: " + time.ctime(stime)
		
		with open(self.listing_document_path, 'r') as f:
			lines = [line.strip() for line in f]
			lines = [line for line in lines[2:] if line]
			
			document_id = ''
			for line in lines:
				elements = line.split(' ')
				if elements[0] == '#':
					document_id = elements[3]
					continue
				
				c_id, category = self._get_category(elements[0])
				
				if category == 'NA':
					continue
				
				if c_id in cob.category_done_list and \
						not self.ignore_duplicate_category:
					continue
				
				sample = self._get_features(fob, elements[1:])
				sample['Category'] = category
				sample['Id'] = document_id

				self.samples = self.samples.append(sample, ignore_index=True)
				
				print "Document #" + document_id + " parsed"

			self.samples = self.samples.fillna(0)
		
		etime = time.time()
		print "Documents in " + self.exp + ' parsed'
		print "End time: " + time.ctime(etime)
		print "Time taken: " + str(etime - stime) + " seconds"

		cob.update_category_done_list([self.category_id1, self.category_id2])
		
		fob.destroy_list()

	def save_samples(self):
		self.parse_all_docs()
		
		if len(self.samples) > 0:
			pickle.dump(self.samples, open(self.samples_data_object_path, 'wb'))

if __name__ == '__main__':
	ob = Document('Exp_1092_135724', ignore_duplicate_category=True)
	ob.save_samples()

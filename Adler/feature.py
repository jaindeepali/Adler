import os
import pickle


class Feature():

	def __init__(self, exp):
		dir = os.path.dirname(__file__)
		self.exp = exp
		self.listing_document_path = os.path.join(
			dir, 'data', 'techtc300_preprocessed',
			exp, 'features.idx')
		self.listing_data_object_path = os.path.join(
			dir, 'data_objects',
			self.exp + '_feature_list.p')
		self.feature_list = []

	def from_id(self, id):
		if not self.feature_list:
			if os.path.exists(self.listing_data_object_path):
				self.feature_list = pickle.load(
					open(self.listing_data_object_path))
			else:
				self.save_list()
		return self.feature_list[id]

	def get_list(self):
		with open(self.listing_document_path, 'r') as f:
			lines = [line.strip() for line in f]
			lines = [line for line in lines if (line and line[0] != '#')]
			self.feature_list = [l.split(' ')[1] for l in lines]

	def save_list(self):
		self.get_list()
		pickle.dump(self.feature_list, open(
			self.listing_data_object_path, 'wb'))

if __name__ == '__main__':
	ob = Feature('Exp_1622_42350')
	ob.save_list()
	print ob.from_id(23)

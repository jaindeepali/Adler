import pickle
import os

class Feature():

	def __init__(self, exp):
		self.exp = exp
		self.listing_document_path = os.path.join('data', 'techtc300_preprocessed', exp, 'features.idx')
		self.listing_data_object_path = os.path.join('data_objects', self.exp + '_feature_list.p')
		self.feature_list = []

	def from_id(self, id):
		if os.path.exists(self.listing_data_object_path):
			self.feature_list = pickle.load(open(self.listing_data_object_path))
		else:
			self.get_list()
		return self.feature_list[id]

	def get_list(self):
		with open(self.listing_document_path, 'r') as f:
			lines = [line.strip() for line in f]
			lines = [line for line in lines if (line and line[0] != '#')]
			self.feature_list = [l.split(' ')[1] for l in lines]
		return

	def save_list(self):
		self.get_list()
		pickle.dump(self.feature_list, open(self.listing_data_object_path, 'wb'))
		return

if __name__ == '__main__':
	ob = Feature('Exp_1622_42350')
	ob.save_list()
	print ob.from_id(23)
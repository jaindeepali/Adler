import pickle
import os

class Feature():

	def __init__(self, exp):
		dir = os.path.dirname(__file__)
		self.exp = exp
		self.listing_document_path = os.path.join(dir, 'data', 'techtc300_preprocessed', exp, 'features.idx')
		self.listing_data_object_path = os.path.join(dir, 'data_objects', self.exp + '_feature_list.p')
		self.feature_list = []

	def fromId(self, id):
		if len(self.feature_list) == 0:
			if os.path.exists(self.listing_data_object_path):
				self.feature_list = pickle.load(open(self.listing_data_object_path))
			else:
				self.saveList()
		return self.feature_list[id]

	def getList(self):
		with open(self.listing_document_path, 'r') as f:
			lines = [line.strip() for line in f]
			lines = [line for line in lines if (line and line[0] != '#')]
			self.feature_list = [l.split(' ')[1] for l in lines]
		return

	def saveList(self):
		self.getList()
		pickle.dump(self.feature_list, open(self.listing_data_object_path, 'wb'))
		return

if __name__ == '__main__':
	ob = Feature('Exp_1622_42350')
	ob.saveList()
	print ob.fromId(23)
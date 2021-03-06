import os
import glob
import time
import pickle

import pandas as pd
from sklearn.feature_selection import SelectKBest, chi2

from Adler import Base, Document, Category

BaseOb = Base()
CatOb = Category()

def download_data():
	BaseOb.fetch_data()

def save_all_samples():
	file_list = os.listdir(BaseOb.raw_data_path)
	for idx, exp in enumerate(file_list):
		
		print "File #" + str(idx)

		sample_path = os.path.join(BaseOb.samples_path, exp + '_samples.p')
		if not os.path.exists(sample_path):
			doc = Document(exp, ignore_duplicate_category=False)
			doc.save_samples()

def merge_samples():

	stime = time.time()
	print 'Merging samples...'
	print "Start time: " + time.ctime(stime)
	
	categories = CatOb.categories
	for category in categories:
		print 'Processing category ' + category
		samples = pd.DataFrame()
		
		sample_files = glob.glob(os.path.join(BaseOb.samples_path, '*'))
		for sample_file in sample_files:
			
			cat_id1 = sample_file.split('_')[-3]
			cat_id2 = sample_file.split('_')[-2]
			
			if CatOb.from_id(cat_id1) == category or \
				CatOb.from_id(cat_id2) == category:
				
				sample = pickle.load(open(sample_file))
				sample = sample.loc[sample['Category'] == category]

				s = sample.sum(numeric_only=True)

				# Keep only half most frequent features
				sample = sample[s[ s >= max(s.median(), 1) ].index]

				sample['Category'] = category
				samples = samples.append(sample, ignore_index=True)
		
		samples = samples.fillna(0)
		_save_dataset(samples, os.path.join('final_dataset', category))
	
	etime = time.time()
	print 'Samples merged'
	print "End time: " + time.ctime(etime)
	print "Time taken: " + str(etime - stime) + " seconds"

def _save_dataset(data, name):
	print 'Saving dataset...'
	destination = BaseOb.data_path
	data.to_csv(os.path.join(destination, name + '.csv'))
	print 'Dataset saved'

def feature_selection():
	
	stime = time.time()
	print 'Selecting features...'
	print "Start time: " + time.ctime(stime)

	samples = pd.DataFrame()
	
	data_files = glob.glob(os.path.join(BaseOb.final_dataset_path, '*'))
	for data_file in data_files:

		data = pd.read_csv(data_file, index_col=0)
		
		category = data['Category'][0]
		print 'Processing ' + category
		print str(data.shape[0]) + ' documents'

		sum_vector = data.sum(numeric_only=True)
		if sum_vector.min() == 1 :
			sum_vector = sum_vector[sum_vector >= sum_vector.median()]
		
		# count_vector = data[data != 0].count(numeric_only=True)
		# count_vector = count_vector[sum_vector.index]
		# count_vector = count_vector / data.shape[0]

		sample = sum_vector
		sample['Category'] = category
		samples = samples.append(sample, ignore_index=True)

	
	samples = samples.fillna(0)
	samples.index = samples['category']
	del samples['category']
	sum_vector = samples.sum()

	# Remove very frequent and very rare words
	s1 = sum_vector[sum_vector <= sum_vector.quantile(0.999)]
	s2 = s2[s2 >= s2.quantile(0.2)]
	samples = samples.loc[:, s2.index]

	# Chi2 feature selection
	feature_selector = SelectKBest(chi2, k=50000)
	feature_selector.fit(samples, range(0, 12)) 
	feature_scores = pd.DataFrame(feature_selector.scores_)
	feature_scores.index = samples.columns

	x = feature_selector.get_support()
	selected_features = pd.DataFrame(samples.columns[x])

	_save_dataset(selected_features, 'selected_features')
	_save_dataset(feature_scores, 'feature_scores')

	etime = time.time()
	print 'Features selected'
	print "End time: " + time.ctime(etime)
	print "Time taken: " + str(etime - stime) + " seconds"

def create_dataset():

	stime = time.time()
	print 'Creating dataset...'
	print "Start time: " + time.ctime(stime)
	
	samples = pd.DataFrame()
	
	feature_file = os.path.join(BaseOb.data_path, 'selected_features.csv')
	selected_features = pd.read_csv(feature_file, index_col=0)
	selected_features = set(selected_features['feature'])

	data_files = glob.glob(os.path.join(BaseOb.final_dataset_path, '*'))
	for data_file in data_files:
		
		sample = pd.read_csv(data_file, index_col=0)

		category = sample['Category'][0]

		print category + ' ' + str(sample.shape[0])

		col = set(sample.columns)
		sample = sample.ix[:, selected_features.intersection(col)]

		samples = samples.append(sample, ignore_index=True)
	
	samples = samples.fillna(0)
	_save_dataset(samples, 'final_dataset')
	
	etime = time.time()
	print 'Database created'
	print "End time: " + time.ctime(etime)
	print "Time taken: " + str(etime - stime) + " seconds"

def main():
	# download_data()
	# save_all_samples()
	# merge_samples()
	create_dataset()
	# feature_selection()

if __name__ == '__main__':
	main()
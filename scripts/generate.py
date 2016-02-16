import os
import glob
import time
import pickle

import pandas as pd

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
				sample = sample[s[ s >= max(s.median(), 0) ].index]

				sample['Category'] = category
				samples = samples.append(sample, ignore_index=True)
		
		samples = samples.fillna(0)
		save_dataset(samples, category)
	
	etime = time.time()
	print 'Samples merged'
	print "End time: " + time.ctime(etime)
	print "Time taken: " + str(etime - stime) + " seconds"

def save_dataset(data, name):
	print 'Saving dataset...'
	destination = BaseOb.final_dataset_path
	data.to_csv(os.path.join(destination, name + '.csv'))
	print 'Dataset saved'

def main():
	# download_data()
	# save_all_samples()
	merge_samples()
	# save_dataset(data)

if __name__ == '__main__':
	main()
import os
import glob
import time
import pickle

import pandas as pd

from Adler import Base, Document

BaseOb = Base()

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
	
	samples = pd.DataFrame()

	sample_files = glob.glob(os.path.join(BaseOb.samples_path, '*'))
	for sample_file in sample_files:
		sample = pickle.load(open(sample_file))
		samples = samples.append(sample, ignore_index=True)
	samples = samples.fillna(0)
	
	etime = time.time()
	print 'Samples merged'
	print "End time: " + time.ctime(etime)
	print "Time taken: " + str(etime - stime) + " seconds"
	
	return samples

def save_dataset(data):
	print 'Saving dataset...'
	destination = BaseOb.final_dataset_path
	with open(os.path.join(destination, 'final_dataset.csv'), 'a') as f:
		data.to_csv(f, header=False)
	print 'Dataset saved'

def main():
	download_data()
	save_all_samples()
	data = merge_samples()
	save_dataset(data)

if __name__ == '__main__':
	main()
import os
import glob
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
		# if idx == 3:
		# 	return
		sample_path = os.path.join(BaseOb.samples_path, exp + '_samples.p')
		if not os.path.exists(sample_path):
			doc = Document(exp)
			doc.save_samples()

def merge_samples():
	print 'Merging samples...'
	sample_files = glob.glob(os.path.join(BaseOb.samples_path, '*'))
	samples = pd.DataFrame()
	for sample_file in sample_files:
		sample = pickle.load(open(sample_file))
		samples = samples.append(sample, ignore_index=True)
	samples = samples.fillna(0)
	print 'Samples merged'
	return samples

def save_dataset(data):
	print 'Saving dataset...'
	destination = BaseOb.final_dataset_path
	# pickle.dump(data, open(os.path.join(destination, 'final_dataset.p'), 'wb'))
	data.to_csv(os.path.join(destination, 'final_dataset.csv'))
	print 'Dataset saved'

def main():
	download_data()
	save_all_samples()
	data = merge_samples()
	save_dataset(data)

if __name__ == '__main__':
	main()
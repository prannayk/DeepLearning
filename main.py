from __future__ import print_function
#import matplotlib as plt
import numpy as np
import os
import sys
import tarfile
from IPython.display import display, Image
from scipy import ndimage
from sklearn.linear_model import LogisticRegression
from six.moves.urllib.request import urlretrieve
from six.moves import cPickle as pickle

# matplotlib inline

url = "http://commondatastorage.googleapis.com/books1000/"
last_percent_reported = None

def download_progress_hook(count, blockSize, totalSize):
	global last_percent_reported
	percent = int(count * blockSize * 100 / totalSize)
	
	if last_percent_reported != percent :
		if percent % 5 == 0:
			sys.stdout("%s%%"%percent)
			sys.stdout.flush()
		else:
			sys.stdout.write(".")
			sys.stdout.flush()
		
		last_percent_reported = percent
		
def maybe_download(filename, expected_bytes, force=False):
	if force or not os.path.exists(filename):
		print('Attempting to download:', filename)
		filename, _ = urlretrieve(url + filename, filename, reporthook=download_progress_hook)
		print('\nDownload Complete!')
	statinfo = os.stat(filename)
	if statinfo.st_size == expected_bytes:
		print('Found and verified', filename)
	else: 
		raise Exception(
			'Failed to verify ' + filename + '. Can you get to it with a browser?')
	return filename

train_filename = maybe_download('notMNIST_large.tar.gz',247336696)
test_filename = maybe_download('notMNIST_small.tar.gz',8458043)

num_classes = 10
np.random.seed(133)

def maybe_extract(filename, force=False):
	root = os.path.splitext(os.path.splitext(filename)[0])[0]
	if os.path.isdir(root) and not force:
		print ("%s already present - Skipping extraction of %s" %(root,filename))
	else:
		print("Extracting data for %s. This may take a while. Please wait!" %(root))
		tar = tarfile.open(filename)
		sys.stdout.flush()
		tar.extractall()
		tar.close()
	data_folders = [
		os.path.join(root,d) for d in sorted(os.listdir(root))
		if os.path.isdir(os.path.join(root,d))]
	
	if len(data_folders) != num_classes:
			raise Exception('shit happened')
	print(data_folders)
	return data_folders

train_folders = maybe_extract(train_filename)
test_folders = maybe_extract(test_filename)



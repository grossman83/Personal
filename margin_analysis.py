import numpy as np
import csv
from matplotlib import pyplot as plt
# from matplotlib.animation import PillowWriter
import sys
import os
import pdb
# from datetime import datetime, timedelta
# import wavio
# import scipy.interpolate as interp



def get_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths


def row2list(row):
	blah = []
	for k in row:
		try:
			blah.append(int(k))
		except:
			continue
	return blah


if __name__ =='__main__':


	# needs to take in a directory and then count the files in it
	# then smash all the csv's together

	margins = np.zeros([16,16])
	
	infile_path = sys.argv[1]

	file_paths = get_file_paths(infile_path)

	margin_samples = np.zeros((15,15))
	for file_path in file_paths:
		with open(file_path, newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',')
			margin_sample = np.zeros([15,15])
			row_list = []
			for row in spamreader:
				row_list.append(row2list(row))


			margin_sample = np.array((row_list[1:-1]))
			margin_sample = np.delete(margin_sample, 0, axis=1)
		margin_samples = np.dstack((margin_samples, margin_sample))

	margin_means = np.mean(margin_samples[:,:,1:], axis=2)

	cmap = plt.cm.gray
	# Plot the array as a bitmap
	plt.imshow(margin_means, cmap=cmap, vmin=0, vmax=1)
	# plt.axis('off')  # Turn off the axis
	plt.show()

	pdb.set_trace()
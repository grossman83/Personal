import numpy as np
import csv
from matplotlib import pyplot as plt
import sys
import os
import pdb
from datetime import datetime, timedelta


if __name__ =='__main__':
	
	infile_path = sys.argv[1]
	outfile_path = sys.argv[2]

	root_path = os.path.expanduser('~')
	infile_path = os.path.join(root_path, infile_path)
	outfile_path = os.path.join(root_path, outfile_path)


	with open(infile_path, newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		timestamp = []
		decimals = []
		rawtime = []
		ax = []
		ay = []
		az = []
		for row in spamreader:
			timestamp.append(datetime.strptime(row[0][0:-2], '%Y-%m-%d %H:%M:%S'))
			rawtime.append(row[0])
			decimals.append(np.int(row[0][-1]))
			ax.append(float(row[2]))
			ay.append(float(row[3]))
			az.append(float(row[4]))

		ax = np.array(ax)
		ay = np.array(ay)
		az = np.array(az)
		# pdb.set_trace()

		# now for a little time math to properly space all the captured data
		# in the time domain.
		decimals = np.array(decimals)
		dt = np.diff(decimals)
		dt = dt.tolist()
		first_micros = decimals[0]
		first_jump_index = min(dt.index(1), dt.index(-9))
		dt.reverse()
		last_jump_index = min(dt.index(1), dt.index(-9))
		last_micros = decimals[-1]

		dt0 = timedelta(microseconds= (int(first_micros)*100000 + (10 - first_jump_index) * 10000))
		dt_ = timedelta(microseconds= (int(last_micros)*100000 + last_jump_index*10000))

		start_time = timestamp[0] + dt0
		end_time = timestamp[-1] + dt_

		rec_time = end_time-start_time

		interval_us = int((rec_time.seconds * 1000000 + rec_time.microseconds)/len(timestamp))

		new_times = []
		for k in range(len(timestamp)):
			new_times.append(timestamp[0] + timedelta(microseconds=interval_us*k))


		#now that we have a start time and an end time and hence a total delta
		#let's evenly spread every point between the start and the end.



		#count the number of same decimals on the first data points


		# timestamp = np.array(datetime.strptime(k[0:-2], '%Y-%m-%d %H:%M:%S') for k in date)
	pdb.set_trace()
	# foo = datetime.strptime(blah, '%y-%m-%d %H:%M:%S')

	#import the csv and read it
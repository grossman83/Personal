import numpy as np
import csv
from matplotlib import pyplot as plt
import sys
import os
import pdb
from datetime import datetime, timedelta
import wavio
import scipy.interpolate as interp


if __name__ =='__main__':
	
	infile_path = sys.argv[1]
	# outfile_path = sys.argv[2]

	root_path = os.path.expanduser('~')
	infile_path = os.path.join(root_path, infile_path)
	# outfile_path = os.path.join(root_path, outfile_path)


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

		date_str = timestamp[0].strftime("%Y-%m-%d %H_%M_%S")

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


		#now that we have a start time and an end time and hence a total delta
		#let's evenly spread every point between the start and the end.
		new_times = []
		for k in range(len(timestamp)):
			new_times.append(timestamp[0] + timedelta(microseconds=interval_us*k))

		zero_start_times = []
		for k in range(len(timestamp)):
			zero_start_times.append(interval_us*k)


		a_rms = np.sqrt(ax**2 + ay**2 + az**2)


		#we're going to create a sound file to show the accelerations
		#experienced by the test berry.
		rate = 44100 #samples per second
		T = rec_time.seconds + rec_time.microseconds / 1000000
		f = 1000.0 # sound frequency [Hz]
		t = np.linspace(0, T, int(T*rate))
		x=0.3 * np.sin(2*np.pi*f*t)

		#now reinterpolate the accelerations onto the length array as the sound
		#data.
		zero_start_times = []
		for k in range(len(timestamp)):
			zero_start_times.append(interval_us*k/1000000)
		a_interp = interp.interp1d(zero_start_times, a_rms, kind='linear', fill_value='extrapolate')

		#now re-interpolate along the time range in the audio
		a_audio = a_interp(t)

		mixed = a_audio * x



		fig = plt.figure(figsize=(18,10))
		ax = fig.add_subplot(1,1,1)
		ax.set_title("Acceleration vs Time")
		ax.set_xlabel("Time [s]")
		ax.set_ylabel("RMS Acceleration [g]")
		ax.plot(zero_start_times, a_rms)
		ax.grid(axis='x', which='major')
		ax.grid(axis='x', which='minor')
		plt.savefig(date_str + ".png")
		# plt.show()
		# ax.plot(t, mixed)



		# pdb.set_trace()

		wavio.write(date_str + ".wav", mixed, rate, sampwidth=3)





		# timestamp = np.array(datetime.strptime(k[0:-2], '%Y-%m-%d %H:%M:%S') for k in date)
	# pdb.set_trace()
	# foo = datetime.strptime(blah, '%y-%m-%d %H:%M:%S')

	#import the csv and read it
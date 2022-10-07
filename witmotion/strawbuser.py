import numpy as np
import csv
from matplotlib import pyplot as plt
from matplotlib.animation import PillowWriter
import sys
import os
import pdb
from datetime import datetime, timedelta
import wavio
import scipy.interpolate as interp


if __name__ =='__main__':
	
	infile_path = sys.argv[1]

	root_path = os.path.expanduser('~')
	infile_path = os.path.join(root_path, infile_path)


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

		date_str = timestamp[0].strftime("%Y-%m-%d %H_%M_%S")


		# it appears that the captured data may vary significantly in capture
		# rate and that this variation is inconsistent. I'm going to make
		# all the timestamp correct by adding the decimals to them.

		#chunk tghe data so that I manage chunks of the same timestamp. Then 
		#grab the corresponding decimals.

		#when seconds change... in case there are holes in the data
		dt = [timestamp[i+1] - timestamp[i] for i in range(len(timestamp[0:-1]))]

		#indices where decimals change
		dc = np.array([decimals[i+1] - decimals[i] for i in range(len(decimals[:-1]))])
		dc_changes1 = np.asarray(np.where(dc == 1)[0])
		dc_changes9 = np.asarray(np.where(dc == -9)[0])

		#all indices where the decimal changes
		dc_changes =  np.sort(np.concatenate((dc_changes1, dc_changes9, [-1])))
		dc_changes = dc_changes+1

		#indice pairs of same decimals
		dc_chunks = [[dc_changes[k], dc_changes[k+1]] for k in range(len(dc_changes)-1)]
		dc_chunks.append([dc_chunks[-1][1], len(timestamp)])


		corrected_ts = []
		for chunk in dc_chunks:
			tss = timestamp[chunk[0]:chunk[1]]
			micros = np.linspace(0, 1000000,len(tss), dtype='int', endpoint=False)
			for [ts, micros] in zip(tss, micros):
				ts = ts + timedelta(microseconds = int(micros))
				corrected_ts.append(ts)
		zero_ts = [k - corrected_ts[0] for k in corrected_ts]

		zero_based_times = [k.seconds + k.microseconds/1000000 for k in zero_ts]




		#now that i've got corrected

		# pdb.set_trace()
		# now for a little time math to properly space all the captured data
		# in the time domain.
		# decimals = np.array(decimals)
		# dt = np.diff(decimals)
		# dt = dt.tolist()
		# first_micros = decimals[0]
		# first_jump_index = min(dt.index(1), dt.index(-9))
		# dt.reverse()
		# last_jump_index = min(dt.index(1), dt.index(-9))
		# last_micros = decimals[-1]

		# dt0 = timedelta(microseconds= (int(first_micros)*100000 + (10 - first_jump_index) * 10000))
		# dt_ = timedelta(microseconds= (int(last_micros)*100000 + last_jump_index*10000))

		# start_time = timestamp[0] + dt0
		# end_time = timestamp[-1] + dt_

		# rec_time = end_time-start_time

		# interval_us = int((rec_time.seconds * 1000000 + rec_time.microseconds)/len(timestamp))


		#now that we have a start time and an end time and hence a total delta
		#let's evenly spread every point between the start and the end.
		# new_times = []
		# for k in range(len(timestamp)):
		# 	new_times.append(timestamp[0] + timedelta(microseconds=interval_us*k))

		# zero_start_times = []
		# for k in range(len(timestamp)):
		# 	zero_start_times.append(interval_us*k)


		a_rms = np.sqrt(ax**2 + ay**2 + az**2)
		rec_time = np.max(zero_based_times)


		#we're going to create a sound file to show the accelerations
		#experienced by the test berry.
		rate = 44100 #samples per second
		# T = rec_time.seconds + rec_time.microseconds / 1000000
		T = rec_time
		f = 800.0 # sound frequency [Hz]
		t = np.linspace(0, T, int(T*rate))
		x=0.1 * np.sin(2*np.pi*f*t)

		#now reinterpolate the accelerations onto the length array as the sound
		#data.
		# zero_start_times = []
		# for k in range(len(timestamp)):
		# 	zero_start_times.append(interval_us*k/1000000)
		
		zero_start_times = zero_based_times

		a_interp = interp.interp1d(zero_start_times, a_rms, kind='linear', fill_value=0)

		#now re-interpolate along the time range in the audio
		a_audio = a_interp(t)
		mixed = a_audio * x
		wavio.write(date_str + ".wav", mixed, rate, sampwidth=3)

		# pdb.set_trace()


		fig = plt.figure(figsize=(8,6))
		ax = fig.add_subplot(1,1,1)
		ax.set_title("Acceleration vs Time")
		# ax.set_xlabel("Time [s]")
		ax.set_ylim([0,30])
		ax.set_ylabel("RMS Acceleration [g]")
		ax.plot(zero_start_times, a_rms, '-b')
		plt.savefig(date_str + ".png", transparent = False)



		video_duration = np.max(zero_start_times)
		fps = 29.97
		num_frames = int(video_duration*fps)
		pts_per_frame = len(a_rms)/num_frames
		pts_per_second = fps*pts_per_frame
		fps=1


		# creating gif so I can overlay it with the video
		metadata = dict(title='Movie', artist='Marc')
		writer = PillowWriter(fps=fps, metadata=metadata)


		with writer.saving(fig, date_str + '.gif', 100):
			first_pt = 0
			for xval in range(int(max(zero_start_times))):
			# for xval in range(100):
				writer.grab_frame(transparent = True)
				scatter = ax.plot([xval], [1], '.r')
				print(xval/max(zero_start_times))

		






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
	
	infile_path0 = sys.argv[1]
	infile_path1 = sys.argv[2]
	infile_path2 = sys.argv[3]
	infile_path3 = sys.argv[4]

	root_path = os.path.expanduser('~')
	infile_path0 = os.path.join(root_path, infile_path0)


	with open(infile_path0, newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		timestamp = []
		decimals = []
		ax = []
		ay = []
		az = []

		w_timestamp = []
		alpha = []
		beta = []
		gamma = []
		for row in spamreader:
			# pdb.set_trace()
			if(len(row) > 5):
				timestamp.append(datetime.strptime(row[0][0:-2], '%Y-%m-%d %H:%M:%S'))
				decimals.append(np.int(row[0][-1]))
				az.append(float(row[4]))
				ay.append(float(row[3]))
				ax.append(float(row[2]))

				try:
					gamma.append(float(row[16]))
					beta.append(float(row[15]))
					alpha.append(float(row[14]))
					
					# w_timestamp.append(datetime.strptime(row[0][0:-2], '%Y-%m-%d %H:%M:%S'))
				except:
					gamma.append(np.nan)
					beta.append(np.nan)
					alpha.append(np.nan)

		ax = np.array(ax)
		ay = np.array(ay)
		az = np.array(az)
		alpha = np.array(alpha)
		beta = np.array(beta)
		gamma = np.array(gamma)

		date_str = timestamp[0].strftime("%Y-%m-%d %H_%M_%S")

		# it appears that the captured data may vary significantly in capture
		# rate and that this variation is inconsistent. I'm going to make
		# all the timestamp correct by adding the decimals to them.

		#chunk the data so that I manage chunks of the same timestamp. Then 
		#grab the corresponding decimals.

		#when seconds change... in case there are holes in the data
		dt = [timestamp[i+1] - timestamp[i] for i in range(len(timestamp[0:-1]))]

		#indices where decimals change
		dc = np.array([decimals[i+1] - decimals[i] for i in range(len(decimals[:-1]))])
		dc_changes1 = np.asarray(np.where(dc == 1)[0])
		dc_changes9 = np.asarray(np.where(dc == -9)[0])
		# dc_changes  = np.asarray(np.where(dc != 0)[0])

		#all indices where the decimal changes
		dc_changes =  np.sort(np.concatenate((dc_changes1, dc_changes9, [-1])))
		dc_changes = dc_changes+1

		#indice pairs of same decimals
		dc_chunks = [[dc_changes[k], dc_changes[k+1]] for k in range(len(dc_changes)-1)]
		dc_chunks.append([dc_chunks[-1][1], len(timestamp)])


		corrected_ts = []
		for chunk in dc_chunks:
			tss = timestamp[chunk[0]:chunk[1]]
			dcs = decimals[chunk[0]:chunk[1]]
			micros = np.linspace(0, 100000,len(tss), dtype='int', endpoint=False)
			for [ts, dc, micro] in zip(tss, dcs, micros):
				ts = ts + timedelta(microseconds = int(micro) + 100000*dc)
				corrected_ts.append(ts)
		zero_ts = [k - corrected_ts[0] for k in corrected_ts]

		zero_based_times = [k.seconds + k.microseconds/1000000 for k in zero_ts]

		a_rms = np.sqrt(ax**2 + ay**2 + az**2)
		# a_rms = np.convolve(a_rms, np.ones(5)/5, mode='same')
		w_rms = np.sqrt(alpha**2 + beta**2 + gamma**2) * np.pi/180.
		w_rms = np.convolve(w_rms, np.ones(100)/100, mode='same')
		rec_time = np.max(zero_based_times)


		#we're going to create a sound file to show the accelerations
		#experienced by the test berry.
		rate = 44100 #samples per second
		T = rec_time
		f = 800.0 # sound frequency [Hz]
		t = np.linspace(0, T, int(T*rate))
		x=0.1 * np.sin(2*np.pi*f*t)
		
		zero_start_times = zero_based_times

		a_interp = interp.interp1d(zero_start_times, a_rms, kind='linear', fill_value=0)

		#now re-interpolate along the time range in the audio
		a_audio = a_interp(t)
		mixed = a_audio * x
		wavio.write(date_str + ".wav", mixed, rate, sampwidth=3)

		# pdb.set_trace()
		plt.ion()
		fig = plt.figure(figsize=(16,9))
		ax = fig.add_subplot(1,1,1)
		ax.set_title("Acceleration vs Time")
		ax.set_ylim([0,30])
		ax.set_ylabel("RMS Acceleration [g]")
		ax.tick_params(axis='y', colors='red')
		ax.yaxis.label.set_color('red')
		secax_y = ax.secondary_yaxis('right')
		secax_y.set_ylabel('Omega [rad/s]')
		secax_y.set_ylim([0,100])
		secax_y.tick_params(axis='y', colors='cyan')
		secax_y.yaxis.label.set_color('cyan')
		ax.plot(zero_start_times, a_rms, '.r', markersize=5)
		ax.plot(zero_start_times, a_rms, '-b', markersize=1)
		ax.plot(zero_start_times, w_rms, '.c', markersize=2)
		plt.savefig(date_str + ".png", transparent = False)

		# plt.show()
		# pdb.set_trace()




		# video_duration = np.max(zero_start_times)
		# fps = 30
		# num_frames = int(np.round(video_duration*fps))
		# pts_per_frame = len(a_rms)/num_frames
		# pts_per_second = fps*pts_per_frame
		fps=1

		# pdb.set_trace()

		# creating gif so I can overlay it with the video
		metadata = dict(title='Movie', artist='Marc')
		writer = PillowWriter(fps=fps, metadata=metadata)

		with writer.saving(fig, date_str + '.gif', 200):
			first_pt = 0
			for xval in range(int(max(zero_start_times))):
				writer.grab_frame(transparent = True)
				scatter = ax.plot([xval], [0], '.g', markersize=10)
				print(xval/max(zero_start_times))
				# plt.show()
				# plt.cla()

		






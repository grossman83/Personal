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
		micros = []
		ax = []
		ay = []
		az = []

		alpha = []
		beta = []
		gamma = []


		for row in spamreader:
			if(len(row) > 5):
				date = datetime.strptime(row[0], '%Y/%m/%d')
				time = datetime.strptime(row[1][0:-3], '%H:%M:%S' )
				micros.append(int(row[2]))
				date.replace(hour=time.hour, minute=time.minute, second=time.second)
				timestamp.append(date)
				az.append(float(row[5])/1000)
				ay.append(float(row[4])/1000)
				ax.append(float(row[3])/1000)

				try:
					gamma.append(float(row[8]))
					beta.append(float(row[7]))
					alpha.append(float(row[6]))
				except:
					gamma.append(np.nan)
					beta.append(np.nan)
					alpha.append(np.nan)

		micros = np.array(micros)
		micros = micros - micros[0]
		ax = np.array(ax)
		ay = np.array(ay)
		az = np.array(az)
		alpha = np.array(alpha)
		beta = np.array(beta)
		gamma = np.array(gamma)

		date_str = timestamp[0].strftime("%Y-%m-%d %H_%M_%S")



		zero_based_times = micros / 1000000.0
		a_rms = np.sqrt(ax**2 + ay**2 + az**2)
		# a_rms = np.convolve(a_rms, np.ones(5)/5, mode='same')
		w_rms = np.sqrt(alpha**2 + beta**2 + gamma**2) * np.pi/180.
		# w_rms = np.convolve(w_rms, np.ones(100)/100, mode='same')
		rec_time = np.max(zero_based_times)

		#we're going to create a sound file to show the accelerations
		#experienced by the test berry.
		rate = 44100 #samples per second
		T = rec_time
		f = 800.0 # sound frequency [Hz]
		t = np.linspace(0, T, int(T*rate))
		x=0.1 * np.sin(2*np.pi*f*t)
		
		zero_start_times = zero_based_times

		data_rate = int(len(zero_based_times)/max(zero_based_times))
		print("Average Data Rate: " + repr(data_rate))

		

		a_interp = interp.interp1d(zero_start_times, a_rms, kind='linear', fill_value=0)

		#now re-interpolate along the time range in the audio
		a_audio = a_interp(t)
		mixed = a_audio * x
		wavio.write(date_str + ".wav", mixed, rate, sampwidth=3)

		plt.ion()
		fig = plt.figure(figsize=(16,9))
		ax = fig.add_subplot(1,1,1)
		ax.set_title("Acceleration vs Time" + "\n" + "Avg Data Rate: " + repr(data_rate) + "Hz")
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

		plt.show()
		pdb.set_trace()

		# video_duration = np.max(zero_start_times)
		# fps = 30
		# num_frames = int(np.round(video_duration*fps))
		# pts_per_frame = len(a_rms)/num_frames
		# pts_per_second = fps*pts_per_frame
		fps=1


		# creating gif so I can overlay it with the video
		metadata = dict(title='Movie', artist='Marc')
		writer = PillowWriter(fps=fps, metadata=metadata)

		with writer.saving(fig, date_str + '.gif', 200):
			first_pt = 0
			for xval in range(int(max(micros/1000000.0))):
				writer.grab_frame(transparent = True)
				scatter = ax.plot([xval], [0], '.g', markersize=10)
				print(xval/max(zero_start_times))
				# plt.show()
				# plt.cla()

		






import csv
import sys
import os
import numpy as np
import json
import copy
import pdb



def readCSV(fullPath):
	blah = []
	with open(fullPath) as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			blah.append(row)

	csvfile.close()
	return blah


def import_json(fullPath):
	with open(fullPath) as fp:
		data = json.load(fp)

	return data


if __name__ == '__main__':
	# fullPath = os.path.join(os.path.expanduser('~'), 'Documents','Output4.csv')
	fullPath = os.path.join(os.path.expanduser('~'), 'Documents', 'Simulation Results', '2R1L_data1.json')

	# blah = readCSV(fullPath)
	data = import_json(fullPath)
	# pdb.set_trace()
	xyzs = data['xyzs']
	angles = data['angles']
	dxyz0 = data['d_xyzs0']
	dxyz1 = data['d_xyzs1']
	dxyz2 = data['d_xyzs2']
	


	# median0 = np.median(np.reshape(dxyz0, (np.shape(dxyz0)[0], np.shape(dxyz0)[1])))
	#get the median values of each set of ratios

	ratio = 5.0
	dtheata_median = []
	for dd in [dxyz0, dxyz1]:
		dtheata_median.append(np.median(np.reshape(dd, (np.shape(dd)[0], np.shape(dd)[1]))))

	dlinear_median = []
	for dd in [dxyz2]:
		dlinear_median.append(np.median(np.reshape(dd, (np.shape(dd)[0], np.shape(dd)[1]))))


	upper_ratios = [k * np.sqrt(ratio) for k in dtheata_median]
	lower_ratios = [k / np.sqrt(ratio) for k in dtheata_median]
	


	#make sure gear ratios are with X of each other, and
	d0_truth_table = np.array([[k>lower_ratios[0] and k<upper_ratios[0] for k in kk] for kk in dxyz0])
	d1_truth_table = np.array([[k>lower_ratios[1] and k<upper_ratios[1] for k in kk] for kk in dxyz1])
	d2_truth_table = np.array([[k>lower_ratios[2] and k<upper_ratios[2] for k in kk] for kk in dxyz2])


	#create mask with all truth tables
	full_mask = d0_truth_table & d1_truth_table & d2_truth_table
	inv_full_mask = np.invert(full_mask)

	#mask the xyz's to remove the points we don't want becasue of ratio
	good_data = np.array(copy.copy(xyzs))
	good_data[~full_mask] = np.nan

	bad_data = np.array(copy.copy(xyzs))
	bad_data[~inv_full_mask] = np.nan

	data_shape = np.shape(xyzs)
	good_pts = np.reshape(good_data, (data_shape[0]*data_shape[1], data_shape[2]))
	bad_pts = np.reshape(bad_data, (data_shape[0]*data_shape[1], data_shape[2]))


	#invert the mask so that we'll have the ability to plot the points that
	#were removed.



	# thetas = data['thetas']
	# xyzs = [eval(k[1]) for k in blah]
	# thetas = [eval(k[0]) for k in blah]
	# pdb.set_trace()
	if len(sys.argv)>1:
		if sys.argv[1] == 'plotly':
			#plot in the cloud using plotly
			import plotly.plotly as py
			import plotly.graph_objs as go
			trace0 = go.Scatter3d(
				x=[k[0] for k in xxyyzzs],
				y=[k[1] for k in xxyyzzs],
				z=[k[2] for k in xxyyzzs],
				mode='markers',
				marker=dict(
					color='rgb(127, 127, 127)',
					size=2,
					symbol='circle',
					line=dict(
						color='rgb(204, 204, 204)',
						width=1
					),
					opacity=0.9
				)
			)
			data = [trace0]
			layout = go.Layout(
				margin=dict(
					l=0,
					r=0,
					b=0,
					t=0
				)
			)
			fig = go.Figure(data=data, layout=layout)
			py.plot(fig, filename='simple-3d-scatter')

	else:
		#plot locally using matplotlib
		import matplotlib as mpl
		mpl.use('TkAgg')
		from mpl_toolkits.mplot3d import Axes3D
		import matplotlib.pyplot as plt

		good_xs = [k[0] for k in good_pts]
		good_ys = [k[1] for k in good_pts]
		good_zs = [k[2] for k in good_pts]

		bad_xs = [k[0] for k in bad_pts]
		bad_ys = [k[1] for k in bad_pts]
		bad_zs = [k[2] for k in bad_pts]


		fig = plt.figure()
		ax = fig.add_subplot(111, projection = '3d')
		ax.scatter(good_xs, good_ys, good_zs, color = 'c')
		ax.scatter(bad_xs, bad_ys, bad_zs, color = 'r')

		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')
		plt.ion()
		plt.show()
		pdb.set_trace()



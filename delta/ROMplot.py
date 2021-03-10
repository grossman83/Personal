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
	fullPath = os.path.join(os.path.expanduser('~'), 'Documents', 'Simulation Results', 'symmetrical2.json')

	# blah = readCSV(fullPath)
	data = import_json(fullPath)
	# pdb.set_trace()
	xyzs = data['xyzs']
	angles = data['angles']
	dxyz0 = data['d_xyzs0']
	dxyz1 = data['d_xyzs1']
	dxyz2 = data['d_xyzs2']
	xyzs = np.array([item for lst in xyzs for item in lst])
	dxyz0 = np.array([item for lst in dxyz0 for item in lst])
	dxyz1 = np.array([item for lst in dxyz1 for item in lst])
	dxyz2 = np.array([item for lst in dxyz2 for item in lst])
	dxyzs = [dxyz0, dxyz1, dxyz2]

	pt_scores = np.max(dxyzs, axis=0) / np.min(dxyzs, axis=0)
	

	#remove all points with scores > than XXX
	max_allowable_score = 20
	trimmed_pt_scores = pt_scores[pt_scores < max_allowable_score]
	trimmed_xyzs = xyzs[pt_scores < max_allowable_score]


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
		import matplotlib.cm as cm
		mpl.use('TkAgg')
		from mpl_toolkits.mplot3d import Axes3D
		import matplotlib.pyplot as plt

		fig = plt.figure()
		ax = fig.add_subplot(111, projection = '3d')
		ax.scatter(trimmed_xyzs[:,0], trimmed_xyzs[:,1], trimmed_xyzs[:,2], c=(100*trimmed_pt_scores/max(trimmed_pt_scores)))

		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')
		plt.ion()
		plt.show()
		pdb.set_trace()



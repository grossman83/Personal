import csv
import sys
import os
import numpy as np
import json

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
	fullPath = os.path.join(os.path.expanduser('~'), 'Documents','data23.json')

	# blah = readCSV(fullPath)
	data = import_json(fullPath)
	# pdb.set_trace()
	xyzs = data['xyzs2']
	data_shape = np.shape(xyzs)
	xxyyzzs = np.reshape(xyzs, (data_shape[0]*data_shape[1], data_shape[2]))
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
		from mpl_toolkits.mplot3d import Axes3D
		import matplotlib.pyplot as plt

		xs = [k[0] for k in xxyyzzs]
		ys = [k[1] for k in xxyyzzs]
		zs = [k[2] for k in xxyyzzs]


		fig = plt.figure()
		ax = fig.add_subplot(111, projection = '3d')
		ax.scatter(xs,ys,zs)
		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')
		plt.ion()
		plt.show()
		pdb.set_trace()



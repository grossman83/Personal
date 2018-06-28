import csv
import os
import plotly.plotly as py
import plotly.graph_objs as go
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
	fullPath = os.path.join(os.path.expanduser('~'), 'Documents','data5.json')

	# blah = readCSV(fullPath)
	data = import_json(fullPath)
	# pdb.set_trace()
	xyzs = data['xyzs']
	thetas = data['thetas']
	# xyzs = [eval(k[1]) for k in blah]
	# thetas = [eval(k[0]) for k in blah]
	pdb.set_trace()

	# x2, y2, z2 = np.random.multivariate_normal(np.array([0,0,0]), np.eye(3), 200).transpose()
	trace0 = go.Scatter3d(
		x=[k[0] for k in xyzs],
		y=[k[1] for k in xyzs],
		z=[k[2] for k in xyzs],
		mode='markers',
		marker=dict(
			color='rgb(127, 127, 127)',
			size=5,
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


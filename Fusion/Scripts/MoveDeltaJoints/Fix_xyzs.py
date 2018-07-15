import numpy as np
import trimesh
import os
import json
import pdb
import time



def import_json(fullPath):
	with open(fullPath) as fp:
		data = json.load(fp)

	return data


def write2json(filePath, data):
	with open(filePath, 'w') as fp:
		# json.dump(data, fp)
		json.dump(data, fp, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == '__main__':
	filepath = os.path.join(os.path.expanduser('~'), 'Documents', 'Simulation Results', 'data1.json')
	data = import_json(filepath)
	xyzs = data['xyzs']
	angles = data['angles']
	d_xyzs0 = data['d_xyzs0']
	d_xyzs1 = data['d_xyzs1']
	d_xyzs2 = data['d_xyzs2']
	free_arm_lengths = data['free_arm_lengths']
	parallel_axes_dist = data['parallel_axes_dist']
	driven_arm_lengths = data['driven_arm_lengths']
	off_axis_joint_position = ['off_axis_joint_position']
	simDuration = data['simDuration']



	pdb.set_trace()
	#now rotate all points about Z axis by +90 degrees because I had the model incorrectly oriented
	R_mat = [[np.cos(t), -np.sin(t), 0],[np.sin(t), np.cos(t), 0],[0,0,1]]

	fixed_xyzs = [np.dot(R_mat, vector) for vector in xyzs]
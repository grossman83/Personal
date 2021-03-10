import numpy as np
import os
import json
import pdb
import math

pi = math.pi



def import_json(fullPath):
	with open(fullPath) as fp:
		data = json.load(fp)

	return data


def write2json(filePath, data):
	with open(filePath, 'w') as fp:
		# json.dump(data, fp)
		json.dump(data, fp, sort_keys=True, indent=4, separators=(',', ': '))




#This was only made because the model I made of the 3R (3 Rotary axes) delta
#is mis-oriented. This fixes the data and saves the data as a .json
#that is formatted exactly the same way as the original.
if __name__ == '__main__':
	filepath = os.path.join(os.path.expanduser('~'), 'Documents', 'Simulation Results', 'data3.json')
	fixed_json_path = os.path.join(os.path.expanduser('~'), 'Documents', 'Simulation Results', 'data3-fixed.json')
	data = import_json(filepath)
	xyzs = data['xyzs']
	angles = data['angles']
	d_xyzs0 = data['d_xyzs0']
	d_xyzs1 = data['d_xyzs1']
	d_xyzs2 = data['d_xyzs2']
	free_arm_lengths = data['free_arm_lengths']
	parallel_axes_dist = data['parallel_axes_dist']
	driven_arm_lengths = data['driven_arm_lengths']
	off_axis_joint_position = data['off_axis_joint_position']
	simDuration = data['simDuration']



	#add back in a bunch of angle data that was not logged as it should have been
	theta0_range = [10.0*k+0.1 for k in range(-7,8)]
	theta0_range = [k*pi/180.0 for k in theta0_range]
	theta1_range = [10.0*k+0.1 for k in range(-7,8)]
	theta1_range = [k*pi/180.0 for k in theta1_range]
	theta2_range = [5*k+0.1 for k in range(-15,16)]
	theta2_range = [k*pi/180.0 for k in theta2_range]

	angles = [[t0, t1, t2] for t0 in theta0_range for t1 in theta1_range for t2 in theta2_range]
	angles = np.reshape(angles, np.shape(xyzs)).tolist()



	pdb.set_trace()
	#now rotate all points about Z axis by +90 degrees because I had the model incorrectly oriented
	t = np.pi/2.0
	R_mat = [[np.cos(t), -np.sin(t), 0],[np.sin(t), np.cos(t), 0],[0,0,1]]

	fixed_xyzs = []
	for list_of_pts in xyzs:
		fixed_xyzs.append([np.dot(R_mat, vector).tolist() for vector in list_of_pts])

	# pdb.set_trace()



	fixed_data = {'xyzs':fixed_xyzs, 'angles':angles, 'd_xyzs0':d_xyzs0, 'd_xyzs1':d_xyzs1, 'd_xyzs2':d_xyzs2,
		'free_arm_lengths': free_arm_lengths,
		'free_arm_lengths': free_arm_lengths,
		'parallel_axes_dist': parallel_axes_dist,
		'driven_arm_lengths': driven_arm_lengths,
		'off_axis_joint_position': off_axis_joint_position,
		'simDuration': simDuration}

	write2json(fixed_json_path, fixed_data)

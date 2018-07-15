import numpy as np
import json
# from tempfile import TemporaryFile
import os
from scipy.interpolate import LinearNDInterpolator
from scipy.interpolate import RegularGridInterpolator
from scipy.optimize import minimize
import pdb


def import_json(fullPath):
	with open(fullPath) as fp:
		data = json.load(fp)
	return data


def write2json(filePath, data):
	with open(filePath, 'w') as fp:
		# json.dump(data, fp)
		json.dump(data, fp, sort_keys=True, indent=4, separators=(',', ': '))


def saveAnglesXYZs2npz(filePath, angles, xyzs):
	# with open(filePath, 'w') as outfile:
	np.savez(filePath, angles, xyzs)


def score_inverse(thetas, des_xyz, FLUT):
	res_xyz = FLUT(thetas)
	return np.linalg.norm(np.array(des_xyz) - res_xyz)


# solve_inverse(xyzs[3000], irreg_FLUT, angles[0])
def solve_inverse(des_xyz, FLUT, t0, search_bounds, the_method):
	X = np.array([1.0, 0, 0])
	Y = np.array([0, 1.0, 0])
	Z = np.array([0, 0, 1.0])
	t0 = np.array(t0)
	dt = 0.001

	if the_method == "Nelder-Mead":
		init_simplex = np.array([t0, dt * X + t0, dt * Y + t0, dt * Z + t0])
		opts_dict = {"disp": False, "initial_simplex": init_simplex}
		# result = minimize(score_inverse, t0, args=(des_xyz, FLUT), method='Nelder-Mead', callback=the_callback, options=opts_dict)
		result = minimize(score_inverse, t0, args=(des_xyz, FLUT), method='Nelder-Mead', options=opts_dict)
		return result

	elif the_method == 'SLSQP':
		# Bounds for variables (only for L-BFGS-B, TNC and SLSQP).
		opts_dict = {"disp": False, "eps": 1.0e-7}
		result = minimize(score_inverse, t0, args=(des_xyz, FLUT), method='SLSQP', bounds=search_bounds, options=opts_dict)
		return result

	elif the_method == "COBYLA":
		disp = False
		catol = 0.02
		maxiter = 10000
		rhobeg = 0.0005
		opts_dict = {"disp": disp, "catol": catol, "maxiter": maxiter, "rhobeg": rhobeg}
		result = minimize(score_inverse, t0, args=(des_xyz, FLUT), method='COBYLA', options=opts_dict)
		return result

	elif the_method == "Newton-CG":
		opts_dict = {"xtol": 1e-3, "eps": 1e-4, "maxiter": 3000}
		result = minimize(score_inverse, t0, args=(des_xyz, FLUT), method='Newton-CG', options=opts_dict)
		return result

	elif the_method == 'TNC':
		# Truncated Newton method.
		# This appears to work OK, but it's looking like minimizers aren't quite the right solution.
		# We are not actually looking for the "minimum" of the objective function. We're actually
		# looking for the objective function to be zero and if it is not then we don't actually
		# have a solve.
		# FLUT table with no bounds error, and a fill value of 0. Should try to move fill val to nan or inf or something

		# workign adequately with: opts_dict = {'eps':0.0001, 'disp':False, 'tol':0.05, 'maxiter':10000, 'xtol':0.0001, 'stepmx':0.005}
		opts_dict = {'eps': 0.0001, 'disp': False, 'tol': 0.05, 'maxiter': 150, 'xtol': 0.0001, 'stepmx': 0.005}
		result = minimize(score_inverse, t0, args=(des_xyz, FLUT), method=the_method, bounds=search_bounds, options=opts_dict)
		return result


def the_callback(xk):
	print("callback: {}".format(xk))


def check_FLUT(FLUT, thetas, xyzs, num_pts):
	idxs = [np.random.randint(0, len(xyzs)) for k in range(num_pts)]

	deltas = []
	for idx in idxs:
		xyz = FLUT(thetas[idx])
		deltas.append(np.linalg.norm(xyz - xyzs[idx]))

	return np.min(deltas), np.max(deltas), np.mean(deltas)


def check_solve(xyzs, angles, FLUT, search_bounds, the_method, num_checks):
	idxs = []
	_angles = []
	for _ in range(num_checks):
		try:
			idx = np.random.randint(0, len(xyzs) - 5)
			result = solve_inverse(xyzs[idx], FLUT, [0, 0, 0], search_bounds, the_method)
			_angles.append(result.x)
			idxs.append(idx)
		except:
			pdb.set_trace()

	# pdb.set_trace()
	res_angles = np.array(_angles)
	the_angles = np.array(angles[idxs])

	deltas = [k[0] - k[1] for k in zip(res_angles, the_angles)]
	norms = np.linalg.norm(deltas, axis=1)
	# pdb.set_trace()

	return np.min(norms), np.max(norms), np.mean(norms)


if __name__ == '__main__':
	filepath = os.path.join(os.path.expanduser('~'), 'Documents', 'Simulation Results', 'data1-fixed.json')
	npzpath = os.path.join(os.path.expanduser('~'), 'Documents', 'Simulation Results', 'data1-fixed.npz')
	data = import_json(filepath)
	_xyzs = data['xyzs']
	_angles = data['angles']
	# sweep_angles = data['sweep_angles']

	xyzs = np.array([item for lst in _xyzs for item in lst])
	angles = np.array([item for lst in _angles for item in lst])


	pdb.set_trace()

	# make the forward lookup table from the irregular data
	irreg_FLUT = LinearNDInterpolator(angles, xyzs)

	# now create a regular lookup table using the irregular table
	# determine minima and maxima of the data
	maxs = np.max(angles, axis=0)
	mins = np.min(angles, axis=0)

	# create regular grid of N points between the mins and maxs
	t0s = np.linspace(mins[0], maxs[0], 20)
	t1s = np.linspace(mins[1], maxs[1], 20)
	t2s = np.linspace(mins[2], maxs[2], 20)

	# Check what function is the fastest at returning information about single points
	# TODO: scipy.ndimage.map_coordinates
	# TODO: scipy.interpolate.interpn
	reg_grid_thetas = np.vstack(np.meshgrid(t0s, t1s, t2s)).reshape(3, -1).T
	reg_grid_xyzs = irreg_FLUT(reg_grid_thetas)
	reg_grid_xyzs = reg_grid_xyzs.reshape((len(t0s), len(t1s), len(t2s), 3))
	reg_FLUT = RegularGridInterpolator([t0s, t1s, t2s], reg_grid_xyzs, method='linear', bounds_error=False, fill_value=np.nan)

	search_bounds = np.array([np.min(angles, axis=0) + 0.005, np.max(angles, axis=0) - 0.005]).T
	# make the inverse lookup table

	the_method = "TNC"
	# result = solve_inverse([0,0,-80.0], reg_FLUT, [0,0,0], search_bounds, the_method)

	# work to calculate the inverse lookup table
	cart_grid_num_pts = 20
	cart_bounds = np.array([np.min(xyzs, axis=0), np.max(xyzs, axis=0)]).T
	xs = np.linspace(*cart_bounds[0], cart_grid_num_pts)
	ys = np.linspace(*cart_bounds[1], cart_grid_num_pts)
	zs = np.linspace(*cart_bounds[2], cart_grid_num_pts)
	xxxyyyzzz = np.vstack(np.meshgrid(xs, ys, zs)).reshape(3, -1).T

	inverses = []
	# the_min, the_max, the_mean = check_solve(xyzs, angles, reg_FLUT, search_bounds, the_method, 50)
	for idx, xyz in enumerate(xxxyyyzzz):
		print("loop count: {}".format(idx))
		result = solve_inverse(xyz, reg_FLUT, [0, 0, 0], search_bounds, the_method)
		try:
			result = solve_inverse(xyz, reg_FLUT, [0, 0, 0], search_bounds, the_method)
			if result.fun > 0.2:
				inverses.append(np.array(3 * [np.nan]))
			else:
				inverses.append(result.x)
		except:
			inverses.append(np.array(3 * [np.nan]))

	# inverses is now the theta's from the solve for given xyz points. There are many
	# xyz points that do not result in an acceptable solve. The results of poor solves
	# are recorded in inverses as 3*[np.nan] so that every point in xxxyyyzzz is mapped
	# to a solution even if the solution is 3*[np.nan]

	# create both types of lookup tables (regular and irregular)
	irreg_ILUT = LinearNDInterpolator(xxxyyyzzz, inverses)
	reg_ILUT = RegularGridInterpolator([xs, ys, zs], np.reshape(inverses, [len(xs), len(ys), len(zs), - 1]), bounds_error=False, fill_value=np.nan)

	# get the computed angles for the xxxyyyzzz's passed into the solver that resulted in.
	# valid solutions. Not all xxxyyyzzz's result in a valid solution.
	re_angles = np.array([k for k in inverses if not any(np.isnan(k))])

	import matplotlib as mpl
	import matplotlib.cm as cm
	mpl.use('TkAgg')
	from mpl_toolkits.mplot3d import Axes3D
	import matplotlib.pyplot as plt

	pdb.set_trace()
	re_angles = irreg_ILUT(xxxyyyzzz)
	fig = plt.figure()
	plt.ion()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(re_angles[:, 0], re_angles[:, 1], re_angles[:, 2], c='b')
	ax.scatter(angles[:, 0], angles[:, 1], angles[:, 2], c='g')
	plt.show()

	pdb.set_trace()

	# speed test the regular forward lookup table
	# pdb.set_trace()
	# rand_pt_qty = 10000
	# nts0 = np.random.rand(rand_pt_qty) * [maxs[0]-mins[0]] - abs(mins[0])
	# nts1 = np.random.rand(rand_pt_qty) * [maxs[1]-mins[1]] - abs(mins[1])
	# nts2 = np.random.rand(rand_pt_qty) * [maxs[2]-mins[2]] - abs(mins[2])

	# testthetas = np.array([nts0, nts1, nts2]).T

	# ########## CALC INVERSE KINEMATICS #############
	# starting from center of original xyz point cloud formed from simulation
	# form a meshgrid that spans all the points of interest. These points
	# span from min(xyz) to max(xyz) of the original points on a regular grid.

	# for each point, start out at some known thetas, in the middle of the thetas.
	# check the cartesian derivative for movement of each of the thetas.
	# move some amount

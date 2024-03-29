import numpy as np
import trimesh
import os
import json
import pdb
import time
import sys
import itertools
import scipy.interpolate



cm2in = 1.0/2.54
in2cm = 1.0/cm2in



##### COPIED FROM STACKOVERFLOW USER Brian Khuu #############
def update_progress(progress):
	barLength = 20 # Modify this to change the length of the progress bar
	status = ""
	if isinstance(progress, int):
		progress = float(progress)
	if not isinstance(progress, float):
		progress = 0
		status = "error: progress var must be float\r\n"
	if progress < 0:
		progress = 0
		status = "Halt...\r\n"
	if progress >= 1:
		progress = 1
		status = "Done...\r\n"
	block = int(round(barLength*progress))
	text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), round(progress*100, 1), status)
	sys.stdout.write(text)
	sys.stdout.flush()
##### COPIED FROM STACKOVERFLOW ############



def rotatePts(pts, axis, theta):
	c = np.cos(theta)
	s = np.sin(theta)

	if axis == [1, 0, 0]:
		Rmat = [[1, 0, 0],[0, c, -s], [0, s, c]]
	elif axis == [0, 1, 0]:
		Rmat = [[c, 0, s],[0, 1, 0], [-s, 0, c]]
	elif axis == [0, 0, 1]:
		Rmat = [[c, -s, 0], [s, c, 0], [0, 0, 1]]
	else:
		Rmat = np.identity_matrix(4)

	if isinstance(pts, list):
		pts = np.ndarray(pts)
	elif isinstance(pts, np.ndarray):
		pass
	
	return np.dot(Rmat, pts.transpose()).transpose().tolist()



def import_json(fullPath):
	with open(fullPath) as fp:
		data = json.load(fp)

	return data

def write2json(filePath, data):
	with open(filePath, 'w') as fp:
		# json.dump(data, fp)
		json.dump(data, fp, sort_keys=True, indent=4, separators=(',', ': '))


def get_static_Rmatrix(angles):
	origin, xaxis, yaxis, zaxis = [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]
	I = trimesh.transformations.identity_matrix()
	Rx = trimesh.transformations.rotation_matrix(angles[0], xaxis)
	Ry = trimesh.transformations.rotation_matrix(angles[1], yaxis)
	Rz = trimesh.transformations.rotation_matrix(angles[2], zaxis)
	R = trimesh.transformations.concatenate_matrices(Rx, Ry, Rz)
	# euler = trimesh.transformations.euler_from_matrix(R, 'sxyz')
	return R


def get_Tmatrix(xyz):
	return trimesh.transformations.translation_matrix(xyz)


def get_mesh_score(mesh, pts, pt_scores):
	pts_in_ww = np.ndarray.tolist([trimesh.proximity.signed_distance(mesh, pts) > 0][0])
	
	try:
		pt_idxs_in_ww = [idx for idx, TF in enumerate(pts_in_ww) if TF]
	except:
		pdb.set_trace()
	if not len(pt_idxs_in_ww) > 0:
		return np.inf
	#compare the min and max dxyzs for every point in the work window. The ratio of max/min
	#is the score.
	try:
		highest_ratio = np.max(pt_scores[pt_idxs_in_ww])
		lowest_ratio = np.min(pt_scores[pt_idxs_in_ww])
	except:
		pdb.set_trace()

	return highest_ratio/lowest_ratio


def voxels_filled(voxel_centers, voxel_pitch, pts):
	for vc in voxel_centers:
		z_pts = (pts[:,2] < vc[2] + voxel_pitch/2.0) & (pts[:,2] > vc[2] - voxel_pitch/2.0)
		if not any(z_pts):
			return False
		rem_pts = pts[z_pts]

		y_pts = (rem_pts[:,1] < vc[1] + voxel_pitch/2.0) & (rem_pts[:,1] > vc[1] - voxel_pitch/2.0)
		if not any(y_pts):
			return False
		rem_pts = rem_pts[y_pts]

		x_pts = (rem_pts[:,0] < vc[0] + voxel_pitch/2.0) & (rem_pts[:,0] > vc[0] - voxel_pitch/2.0)
		if not any(x_pts):
			return False

	return True


def get_irreg_voxel_centers(box_center, box_extents, factor):
	#returns box centers that are at the center of the irregular
	#"voxels" that split the original box into factor**3 smaller
	#"voxels"
	v_edge_lens = box_extents / (factor-1)

	new_box_centers = [[box_center[j] - box_extents[j]/2.0 + k * v_edge_lens[j] for k in range(factor)] for j in range(3)]
	xs, ys, zs = new_box_centers

	new_box_centers = np.array([[x,y,z] for x in xs for y in ys for z in zs])

	sub_box_pitches = np.array(box_extents)/factor

	return new_box_centers, sub_box_pitches



def irreg_voxels_filled(voxel_centers, voxel_pitches, pts):
	for vc in voxel_centers:
		# pdb.set_trace()
		z_pts = (pts[:,2] < vc[2] + voxel_pitches[2]/2.0) & (pts[:,2] > vc[2] - voxel_pitches[2]/2.0)
		if not any(z_pts):
			return False
		rem_pts = pts[z_pts]

		y_pts = (rem_pts[:,1] < vc[1] + voxel_pitches[1]/2.0) & (rem_pts[:,1] > vc[1] - voxel_pitches[1]/2.0)
		if not any(y_pts):
			return False
		rem_pts = rem_pts[y_pts]

		x_pts = (rem_pts[:,0] < vc[0] + voxel_pitches[0]/2.0) & (rem_pts[:,0] > vc[0] - voxel_pitches[0]/2.0)
		if not any(x_pts):
			return False

	return True


def resample_data(pts, pt_scores, pitch):
	#get the bounds of the points
	my_pts = trimesh.points.PointCloud(pts)
	bounds = my_pts.bounds
	extents = my_pts.extents
	num_pts = [int(np.ceil(k / pitch)) for k in extents]
	xs = np.linspace(bounds[0][0], bounds[1][0], num_pts[0])
	ys = np.linspace(bounds[0][1], bounds[1][1], num_pts[0])
	zs = np.linspace(bounds[0][2], bounds[1][2], num_pts[0])

	resampled_pts = np.vstack(np.meshgrid(xs, ys, zs)).reshape(3,-1).T
	resampled_pt_scores = scipy.interpolate.griddata(pts, pt_scores, resampled_pts, method='linear', fill_value=10000.0)

	return resampled_pts, resampled_pt_scores





def display_result_by_idx(idx, box_shapes, voxel_pitch, y_axis_rotations, translations, pts):
	# idx = scores.index(min(scores))
	box_mesh = trimesh.creation.box(box_shapes[idx], np.identity(4))
	box_mesh_voxelized = box_mesh.voxelized(voxel_pitch).as_boxes()
	rotated_pts = rotatePts(pts, [0,1,0], y_axis_rotations[idx])
	# center_of_pts = np.median(rotated_pts, axis=0)
	# center_of_pts[2] = center_of_pts[2]*1.5
	# centered_pts = rotated_pts - center_of_pts
	xlated_pts = rotated_pts + translations[idx]
	my_pts = trimesh.points.PointCloud(xlated_pts)
	my_scene = trimesh.scene.scene.Scene()
	my_scene.add_geometry(box_mesh)
	my_scene.add_geometry(box_mesh_voxelized)
	my_scene.add_geometry(my_pts)
	my_scene.show()



def save_results(results_path, scores, box_shapes, voxel_pitch, y_axis_rotations, translations, pts):
	mydata = {'scores':scores,
	'box_shapes':box_shapes,
	'voxel_pitch':voxel_pitch,
	'y_axis_rotations':y_axis_rotations,
	'translations':translations,
	'pts':pts}

	write2json(results_path, mydata)






if __name__ == '__main__':
	filepath = os.path.join(os.path.expanduser('~'), 'Documents', 'Simulation Results', 'data3-fixed.json')
	data = import_json(filepath)
	xyzs = data['xyzs']
	dxyz0 = data['d_xyzs0']
	dxyz1 = data['d_xyzs1']
	dxyz2 = data['d_xyzs2']
	#flatten the lists
	dxyz0 = [item for lst in dxyz0 for item in lst]
	dxyz1 = [item for lst in dxyz1 for item in lst]
	dxyz2 = [item for lst in dxyz2 for item in lst]
	dxyzss = np.array([dxyz0, dxyz1, dxyz2])
	pt_scores = np.max(dxyzss, axis=0)/np.min(dxyzss, axis=0)



	pts = np.reshape(xyzs, (np.shape(xyzs)[0]*np.shape(xyzs)[1], 3))
	pts_center = np.median(pts, axis=0)
	reg_pts, reg_pt_scores = resample_data(pts, pt_scores, 10)




	translations = []
	box_shapes = []
	y_axis_rotations = []
	scores = []
	start_time = time.time()
	loops_nums = [8,3,13,9]
	total_iterations = loops_nums[0]*loops_nums[1]*loops_nums[2]*loops_nums[3]
	loop_count = 0
	#create a box of the desired dimensions at the origin
	#rotate the points by the desired amount about the Y axis.
	#get the "center" of the point cloud and translate it by that amount to place it at the origin
	#Perform translations in X and Z of that point cloud and score the results
	voxel_pitch = 11
	num_divisions = 3
	box_len_x = 30*in2cm
	box_len_y = []
	box_len_z = 15*in2cm
	for box_len_y in np.linspace(50, 60, loops_nums[0]):
		box_mesh = trimesh.creation.box([box_len_x, box_len_y, box_len_z], np.identity(4))
		voxel_centers = box_mesh.voxelized(voxel_pitch).points
		sub_voxel_centers, sub_voxel_pitches = get_irreg_voxel_centers(box_mesh.centroid, box_mesh.extents, num_divisions)
		for theta_y in np.linspace(-np.pi/60, np.pi/60, loops_nums[1]):
			rotated_pts = rotatePts(reg_pts, [0, 1, 0], theta_y)
			orig_pts = rotatePts(pts, [0, 1, 0], theta_y)
			center_of_pts = np.median(orig_pts, axis=0)
			center_of_pts[2] = center_of_pts[2]*1.5
			for Tx in np.linspace(-60, 60, loops_nums[2]):
				for Tz in np.linspace(-40, 40, loops_nums[3]):
					# pdb.set_trace()
					loop_count+=1
					update_progress(loop_count/total_iterations)
					total_translation = np.array([Tx, 0, Tz]) - center_of_pts
					#translate the points by Tx and Ty
					xlated_pts = rotated_pts + total_translation
					orig_pts_xlated = orig_pts + total_translation
					# reg_pts, reg_pt_scores = resample_data(pts, pt_scores, 10)
					#check to see that points are within every voxel of the work window mesh
					if not voxels_filled(voxel_centers, voxel_pitch, xlated_pts):
						break
					# pdb.set_trace()
					# if not irreg_voxels_filled(sub_voxel_centers, sub_voxel_pitches, reg_pts):
					# 	break
					# scores.append(get_mesh_score(box_mesh, xlated_pts, pt_scores))
					scores.append(get_mesh_score(box_mesh, xlated_pts, reg_pt_scores))
					translations.append(total_translation)
					box_shapes.append([box_len_x, box_len_y, box_len_z])
					y_axis_rotations.append(theta_y)
					



# my_scene = trimesh.scene.scene.Scene()
# my_scene.add_geometry(box_mesh)
# my_scene.add_geometry(box_mesh.voxelized(voxel_pitch).as_boxes())
# my_pts = trimesh.points.PointCloud(xlated_pts)
# my_scene.add_geometry(my_pts)
# my_scene.show()




# my_scene = trimesh.scene.scene.Scene()
# my_scene.add_geometry(box_mesh)
# # my_scene.add_geometry(box_mesh.voxelized(20).as_boxes())
# my_pts = trimesh.points.PointCloud(xlated_pts)
# my_orig_pts = trimesh.points.PointCloud(orig_pts_xlated)
# my_scene.add_geometry(my_pts)
# my_scene.add_geometry(my_orig_pts)
# my_scene.show()



# idx = scores.index(min(scores))
# box_mesh = trimesh.creation.box(box_shapes[idx], np.identity(4))
# box_mesh_voxelized = box_mesh.voxelized(voxel_pitch).as_boxes()
# rotated_pts = rotatePts(pts, [0,1,0], y_axis_rotations[idx])
# center_of_pts = np.median(rotated_pts, axis=0)
# center_of_pts[2] = center_of_pts[2]*1.5
# centered_pts = rotated_pts - center_of_pts
# xlated_pts = centered_pts + translations[idx]
# my_pts = trimesh.points.PointCloud(xlated_pts)
# my_scene = trimesh.scene.scene.Scene()
# my_scene.add_geometry(box_mesh)
# my_scene.add_geometry(box_mesh_voxelized)
# my_scene.add_geometry(my_pts)
# my_scene.show()



# my_scene_viewer = trimesh.scene.viewer.SceneViewer(my_scene)
# pt_colors = [(int(k/max(pt_scores)*255),0,0) for k in pt_scores]
# my_pts = trimesh.points.PointCloud(xlated_pts, colors = pt_colors)


					
					# pdb.set_trace()

	pdb.set_trace()

	my_pts = trimesh.points.PointCloud(xlated_pts)
	my_scene = trimesh.scene.scene.Scene()
	my_scene.add_geometry(box_mesh)
	my_scene.add_geometry(my_pts)
	my_scene.show()



	pdb.set_trace()
	#move the work_window_mesh
	# trimesh.apply_transform(matrix)
	my_pts = trimesh.points.PointCloud(pts)
	my_scene = trimesh.scene.scene.Scene()
	my_scene.add_geometry(box_mesh)
	my_scene.add_geometry(my_pts)
	my_scene.show()



	pdb.set_trace()


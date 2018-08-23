import adsk.core, adsk.fusion, traceback, math, copy, operator
import random
import os
import json
import time
#import operator

pi = math.pi

thetas = []
xyzs = []

rootPath = os.path.expanduser('~')
fullPath = os.path.join(rootPath, 'Data', 'output3.csv')
jsonFullPath = 'Documents/data4.json'

app = adsk.core.Application.get()
ui = app.userInterface
design = app.activeProduct


#initialize global parameters
driven_arm_0_length = design.userParameters.itemByName('driven_arm_length').value#cm
driven_arm_1_length = design.userParameters.itemByName('driven_arm_length').value#cm
driven_arm_2_length = design.userParameters.itemByName('off_axis_driven_arm_length').value#cm
driven_arm_lengths = [driven_arm_0_length, driven_arm_1_length, driven_arm_2_length]
parallel_axes_dist = design.userParameters.itemByName('parallel_axes_dist').value
free_arm_length = design.userParameters.itemByName('free_arm_length').value
off_axis_free_arm_length = design.userParameters.itemByName('off_axis_free_arm_length').value
free_arm_lenghts = [free_arm_length, free_arm_length, off_axis_free_arm_length]


#constants
dtheta = 0.001#1mrad


def getDist2Origin(component):
	#Returns the distance between the origin of the component passed in
	#and the root component origin. All distances in cm as per Fusion standards.
	try:
		trans = component.transform.translation
		return [trans.x,trans.y,trans.z]
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def write2json(filePath, data):
	with open(filePath, 'w') as fp:
		# json.dump(data, fp)
		json.dump(data, fp, sort_keys=True, indent=4, separators=(',', ': '))


def abs2rev(theta):
	#the angles of the joints are thought of as + - 60-90 degrees above and
	#below the horizontal. this converts them to how the joint is setup which
	#is between 0 and 180. The reason for this is that fusion does not handle
	#well joints that pass through the 0/360 degree point.
	return theta + pi/2

def rev2abs(theta):
	return theta - pi/2

def setRevoluteJoints(revolute_joints, thetas):
	#successively unlocks, then moves any joint that is not set to the angle desired by thetas
	#NOTES:
	#did not work correctly without both adsk.doEvents() commands at the end
	#does appear to work with the doEvents() after locking and unlocking commented out
	try:
		cur_joint_angles = [rev2abs(k.jointMotion.rotationValue) for k in revolute_joints]
		counter = 0
		while not all(math.isclose(k[0], k[1], abs_tol=0.001) for k in zip(cur_joint_angles, thetas)):
			for idx, joint in enumerate(revolute_joints):
				if joint.jointMotion.rotationValue != abs2rev(thetas[idx]):
					joint.isLocked = False
					joint.jointMotion.rotationValue = abs2rev(thetas[idx])
					joint.isLocked = True
					adsk.doEvents()
			cur_joint_angles = [rev2abs(k.jointMotion.rotationValue) for k in revolute_joints]

			#if the angles are not correct, shuffle them a bit and re-attempt.
			if not all(math.isclose(k[0], k[1], abs_tol=0.001) for k in zip(cur_joint_angles, thetas)):
				temp_thetas = [(k[0]+k[1])/2.0 for k in zip(cur_joint_angles, thetas)]
				for idx, joint in enumerate(revolute_joints):
					if joint.jointMotion.rotationValue != abs2rev(thetas[idx]):
						joint.isLocked = False
						joint.jointMotion.rotationValue = abs2rev(temp_thetas[idx])
						joint.isLocked = True
						adsk.doEvents()

			counter += 1
			if counter > 10:
				break

		adsk.doEvents()
		adsk.doEvents()

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

#test script
# desired_thetas, measured_thetas = test_setRevoluteJoints(revolute_joints)
# [list(map(operator.sub, k[0],k[1])) for k in zip(desired_thetas, measured_thetas)]
def test_setRevoluteJoints(revolute_joints):
	#move randomly between -60, and 60
	desired_thetas = []
	measured_thetas = []
	for k in range(60):
		rand_angles = [random.randint(-60,60) for k in range(3)]
		thetas = [k*pi/180 for k in rand_angles]
		desired_thetas.append(thetas)
		setRevoluteJoints(revolute_joints, thetas)
		measured_thetas.append([rev2abs(j.jointMotion.rotationValue) for j in revolute_joints])

	return desired_thetas, measured_thetas

def sweep_joint(joint_id, revolute_joints, thetas, mobilePlatform):
	#this performs a sweep which is much faster than setting individual angles.
	#It takes in the joint_id that is goign to be swept as an index of it's
	#position in the list of joints revolute_joints. It then takes in list of
	#angles over which to sweep that joint. At each position swept through it
	#logs the angles of all the joints as well as the cartesian position
	#of the mobile platform relative to the root component origin.
	try:
		xyzs = []
		angles = []
		revolute_joints[joint_id].isLocked = False
		adsk.doEvents()
		for theta in thetas:
			revolute_joints[joint_id].jointMotion.rotationValue = abs2rev(theta)
			# adsk.doEvents()
			temp_angles = [rev2abs(j.jointMotion.rotationValue) for j in revolute_joints]
			temp_angles[joint_id] = theta
			angles.append(temp_angles)
			xyzs.append(getDist2Origin(mobilePlatform))
		revolute_joints[joint_id].isLocked = True
		adsk.doEvents()
		return angles, xyzs

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def get_dXYZ_dTheta(revolute_joints, mobilePlatform):
	#returns the norm of the distance between points closely spaced in theta space
	try:	
		dtheta = 0.001 #1mrad
		#get current positions
		orig_thetas = [j.jointMotion.rotationValue for j in revolute_joints]
		orig_pos = getDist2Origin(mobilePlatform)
		dxyzs = []

		for k in range(len(revolute_joints)):
			dthetas = [0.0,0.0,0.0]
			dthetas[k] = dtheta
			setRevoluteJoints(revolute_joints, [k[0]+k[1] for k in zip(orig_thetas, dthetas)])
			cur_pos = getDist2Origin(mobilePlatform)
			dxyz = math.sqrt(math.fsum([(k[1]-k[0])**2 for k in zip(orig_pos, cur_pos)]))
			corrected_dxyz = dxyz/(driven_arm_lengths[k]*dtheta)
			dxyzs.append(corrected_dxyz)
			setRevoluteJoints(revolute_joints, orig_thetas)
		return dxyzs


	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def get_norms(lol_1, lol_2):
	#takes two lists of lists and performs the list-wise norms returning them
	norms = []
	for k in zip(lol_1, lol_2):
		norms.append(math.sqrt(math.fsum([(kk[1]-kk[0])**2 for kk in zip(k[0], k[1])])))
	return norms


def run(context):
	try:
		rootComp = app.activeProduct.rootComponent
		mobilePlatform = rootComp.occurrences.itemByName('Mobile_Platform:1')

		#joint origin of off-axis revolute joint
		off_axis_joint_origin = rootComp.jointOrigins.itemByName('off_axis_joint_origin')
		off_axis_joint_Xdist = off_axis_joint_origin.offsetX.value
		off_axis_joint_Ydist = off_axis_joint_origin.offsetY.value
		off_axis_joint_Zdist = off_axis_joint_origin.offsetZ.value


		rev0 = rootComp.joints.itemByName('Shoulder0_Revolute')
		rev1 = rootComp.joints.itemByName('Shoulder1_Revolute')
		rev2 = rootComp.joints.itemByName('Shoulder2_Revolute')
		revolute_joints = [rev0, rev1, rev2]

		xyzs=[]
		thetas = []

		d_xyzs0 = []
		d_xyzs1 = []
		d_xyzs2 = []


		theta0_range = [5.0*k+0.1 for k in range(-12,13)]
		theta0_range = [k*pi/180.0 for k in theta0_range]
		theta1_range = [5.0*k+0.1 for k in range(-12,13)]
		theta1_range = [k*pi/180.0 for k in theta1_range]


		theta2_range = [2.0*k+0.1 for k in range(-32,11)]
		theta2_range = [k*pi/180 for k in theta2_range]

		enable_dxyzs = False
		

		loop_count = 0
		start_time = time.time()
		for t0 in theta0_range:
			for t1 in theta1_range:
				#set starting positions for all joints
				setRevoluteJoints(revolute_joints, [t0, t1, theta2_range[0]])
				#perform the sweep
				angles, sweep_xyzs = sweep_joint(2, revolute_joints, theta2_range, mobilePlatform)
				xyzs.append(sweep_xyzs)
				thetas.append(angles)

				if enable_dxyzs:
					#now make minor adjustment to the thetas and redo the sweep to get
					#dtheta / norm(dxyz) for each of the three axes.
					setRevoluteJoints(revolute_joints, [t0+dtheta, t1, theta2_range[0]])
					_angles, _xyzs = sweep_joint(2, revolute_joints, theta2_range, mobilePlatform)
					# _norms = get_norms(sweep_xyzs, _xyzs)
					# dtheta_l = dtheta*driven_arm_lengths[0]
					_dxyzs = [[k[0][0] - k[1][0], k[0][1] - k[1][1], k[0][2]-k[1][2]] for k in zip(_xyzs, sweep_xyzs)]
					d_xyzs0.append(_dxyzs)

					setRevoluteJoints(revolute_joints, [t0, t1+dtheta, theta2_range[0]])
					_angles, _xyzs = sweep_joint(2, revolute_joints, theta2_range, mobilePlatform)
					# _norms = get_norms(sweep_xyzs, _xyzs)
					# dtheta_l = dtheta*driven_arm_lengths[1]
					_dxyzs = [[k[0][0] - k[1][0], k[0][1] - k[1][1], k[0][2]-k[1][2]] for k in zip(_xyzs, sweep_xyzs)]
					d_xyzs1.append(_dxyzs)

					setRevoluteJoints(revolute_joints, [t0, t1, theta2_range[0]])
					_angles, _xyzs = sweep_joint(2, revolute_joints, [k+dtheta for k in theta2_range], mobilePlatform)
					# _norms = get_norms(sweep_xyzs, _xyzs)
					# dtheta_l = dtheta*driven_arm_lengths[2]
					_dxyzs = [[k[0][0] - k[1][0], k[0][1] - k[1][1], k[0][2]-k[1][2]] for k in zip(_xyzs, sweep_xyzs)]
					d_xyzs2.append(_dxyzs)



		stop_time = time.time()
		delta_time = stop_time - start_time

		simdata = {'xyzs':xyzs, 'angles':thetas, 'd_xyzs0':d_xyzs0, 'd_xyzs1':d_xyzs1, 'd_xyzs2':d_xyzs2,
		'driven_arm_lengths': driven_arm_lengths,
		'free_arm_lenghts': free_arm_lenghts,
		'parallel_axes_dist': parallel_axes_dist,
		'driven_arm_lengths': driven_arm_lengths,
		'off_axis_joint_position': [off_axis_joint_Xdist, off_axis_joint_Ydist, off_axis_joint_Zdist],
		'simDuration': delta_time}
		
		write2json(jsonFullPath, simdata)
		print(delta_time)
		##########************###########

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



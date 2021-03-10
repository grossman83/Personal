import adsk.core, adsk.fusion, traceback, math, copy, operator, pdb
import random
import os
import json
import time
#import operator

pi = math.pi

thetas = []
xyzs = []

rootPath = os.path.expanduser('~')
fullPath = os.path.join(rootPath, 'Documents', 'output3.csv')
jsonFullPath = 'Documents/2R1L_data3.json'

app = adsk.core.Application.get()
ui = app.userInterface
design = app.activeProduct


#initialize global parameters
driven_arm_0_length = design.userParameters.itemByName('driven_arm_length').value#cm
driven_arm_1_length = design.userParameters.itemByName('driven_arm_length').value#cm
linear_rail_angle = design.userParameters.itemByName('linear_rail_angle').value
driven_arm_lengths = [driven_arm_0_length, driven_arm_1_length]
parallel_axes_dist = design.userParameters.itemByName('parallel_axes_dist').value
off_axis_joint_X = design.userParameters.itemByName('off_axis_joint_X').value
off_axis_joint_Y = design.userParameters.itemByName('off_axis_joint_Y').value
off_axis_joint_Z = design.userParameters.itemByName('off_axis_joint_Z').value
free_arm_length = design.userParameters.itemByName('free_arm_length').value
off_axis_free_arm_length = design.userParameters.itemByName('off_axis_free_arm_length').value
free_arm_lengths = [free_arm_length, free_arm_length, off_axis_free_arm_length]

#pdb.set_trace()

#constants
dtheta = 0.001#1mrad


def getDist2Origin(component):
	#Returns the distance between the origin of the component passed in
	#and the root component origin. All distances in cm as per Fusion standards.
	try:
		trans = component.transform.translation
		return [trans.x,trans.y,trans.z]
	except:
		pdb.set_trace()
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
		for idx, joint in enumerate(revolute_joints):
			# if joint.jointMotion.rotationValue != abs2rev(thetas[idx]):
			if not math.isclose(joint.jointMotion.rotationValue, abs2rev(thetas[idx]), abs_tol = 0.001):
				joint.isLocked = False
				joint.jointMotion.rotationValue = abs2rev(thetas[idx])
				joint.isLocked = True
		adsk.doEvents()
		adsk.doEvents()

	except:
		pdb.set_trace()
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def setSliderJoint(slider_joint, value):
	try:
		if not math.isclose(slider_joint.jointMotion.value, value, abs_tol = 0.05):
			slider_joint.isLocked = False
			slider_joint.jointMotion.slideValue = value
			slider_joint.isLocked = True
		adsk.doEvents()
		adsk.doEvents()
	except:
		pdb.set_trace()
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
			temp_angles = [rev2abs(j.jointMotion.rotationValue) for j in revolute_joints]
			temp_angles[joint_id] = theta
			angles.append(temp_angles)
			xyzs.append(getDist2Origin(mobilePlatform))
		revolute_joints[joint_id].isLocked = True
		adsk.doEvents()
		return angles, xyzs

	except:
		pdb.set_trace()
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def sweep_slider_joint(slider_joint, revolute_joints, values, mobilePlatform):
	#this performs a sweep which is much faster than setting individual angles.
	#It takes in a list of the revolute joints. It then takes in list of
	#distances over which to sweep the slider joint. At each position swept through it
	#logs the angles of the revolute joints as well as the cartesian position
	#of the mobile platform relative to the root component origin.
	try:
		xyzs = []
		angles = []
		slider_joint.isLocked = False
		adsk.doEvents()
		for value in values:
			slider_joint.jointMotion.slideValue = value
			temp_angles = [rev2abs(j.jointMotion.rotationValue) for j in revolute_joints]
			angles.append(temp_angles)
			xyzs.append(getDist2Origin(mobilePlatform))
		slider_joint.isLocked = True
		adsk.doEvents()
		return angles, values, xyzs

	except:
		pdb.set_trace()
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
		pdb.set_trace()
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def get_norms(lol_1, lol_2):
	try:
		#takes two lists of lists and performs the list-wise norms returning them
		norms = []
		for k in zip(lol_1, lol_2):
			norms.append(math.sqrt(math.fsum([(kk[1]-kk[0])**2 for kk in zip(k[0], k[1])])))
		return norms
	except:
		pdb.set_trace()
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def run(context):
	try:
		rootComp = app.activeProduct.rootComponent
		linearRail = rootComp.occurrences.itemByName('Linear Rail:1')
		mobilePlatform = rootComp.occurrences.itemByName('MobilePlatform:1')

		off_axis_joint = rootComp.joints.itemByName('Rigid3')


		rev0 = rootComp.joints.itemByName('Shoulder0_Revolute')
		rev1 = rootComp.joints.itemByName('Shoulder1_Revolute')
		revolute_joints = [rev0, rev1]

		slider_joint = linearRail.joints.itemByName('Slider1')

		xyzs=[]
		thetas = []
		slide_values = []

		d_xyzs0 = []
		d_xyzs1 = []
		d_xyzs2 = []


		theta0_range = [10.0*k+0.1 for k in range(-7,8)]
		theta0_range = [k*pi/180.0 for k in theta0_range]
		theta1_range = [10.0*k+0.1 for k in range(-8,8)]
		theta1_range = [k*pi/180.0 for k in theta1_range]


		# theta2_range = [5.0*k+0.1 for k in range(-15,16)]
		# theta2_range = [k*pi/180 for k in theta2_range]
		slider_range = [k*2.0 for k in range(-5, 16)]


		loop_count = 0
		start_time = time.time()
		for t0 in theta0_range:
			for t1 in theta1_range:
				#set starting positions for all joints
				setRevoluteJoints(revolute_joints, [t0, t1])
				#perform the sweep
				# angles, sweep_xyzs = sweep_joint(2, revolute_joints, theta2_range, mobilePlatform)
				angles, _slide_values, sweep_xyzs = sweep_slider_joint(slider_joint, revolute_joints, slider_range, mobilePlatform)
				xyzs.append(sweep_xyzs)
				slide_values.append(_slide_values)
				thetas.append(angles)


				#now make minor adjustment to the thetas and redo the sweep to get
				#dtheta / norm(dxyz) for each of the three axes.
				setRevoluteJoints(revolute_joints, [t0+dtheta, t1])
				_angles, _slide_values, _xyzs = sweep_slider_joint(slider_joint, revolute_joints, slider_range, mobilePlatform)
				_norms = get_norms(sweep_xyzs, _xyzs)
				dtheta_l = dtheta*driven_arm_lengths[0]
				d_xyzs0.append([dtheta_l/k for k in _norms])

				setRevoluteJoints(revolute_joints, [t0, t1+dtheta])
				_angles, _slide_values, _xyzs = sweep_slider_joint(slider_joint, revolute_joints, slider_range, mobilePlatform)
				_norms = get_norms(sweep_xyzs, _xyzs)
				dtheta_l = dtheta*driven_arm_lengths[0]
				d_xyzs1.append([dtheta_l/k for k in _norms])

				#d_l is the minor adjustment t the original positions of the slider joint so we can calculate dslider/dx/dy/dz
				d_l = 0.1#1mm
				setRevoluteJoints(revolute_joints, [t0, t1])
				_angles, _slide_values, _xyzs = sweep_slider_joint(slider_joint, revolute_joints, [k+d_l for k in slider_range], mobilePlatform)
				_norms = get_norms(sweep_xyzs, _xyzs)
				d_xyzs2.append([d_l/k for k in _norms])




				# setRevoluteJoints(revolute_joints, [t0+dtheta, t1, theta2_range[0]])
				# _angles, _xyzs = sweep_joint(2, revolute_joints, theta2_range, mobilePlatform)
				# _norms = get_norms(sweep_xyzs, _xyzs)
				# dtheta_l = dtheta*driven_arm_lengths[0]
				# d_xyzs0.append([dtheta_l/k for k in _norms])

				# setRevoluteJoints(revolute_joints, [t0, t1+dtheta, theta2_range[0]])
				# _angles, _xyzs = sweep_joint(2, revolute_joints, theta2_range, mobilePlatform)
				# _norms = get_norms(sweep_xyzs, _xyzs)
				# dtheta_l = dtheta*driven_arm_lengths[1]
				# d_xyzs1.append([dtheta_l/k for k in _norms])

				# setRevoluteJoints(revolute_joints, [t0, t1, theta2_range[0]])
				# _angles, _xyzs = sweep_joint(2, revolute_joints, [k+dtheta for k in theta2_range], mobilePlatform)
				# _norms = get_norms(sweep_xyzs, _xyzs)
				# dtheta_l = dtheta*driven_arm_lengths[2]
				# d_xyzs2.append([dtheta_l/k for k in _norms])



		stop_time = time.time()
		delta_time = stop_time - start_time

		simdata = {'xyzs':xyzs, 'angles':angles, 'd_xyzs0':d_xyzs0, 'd_xyzs1':d_xyzs1, 'd_xyzs2':d_xyzs2,
		'driven_arm_lengths': driven_arm_lengths,
		'free_arm_lengths': free_arm_lengths,
		'parallel_axes_dist': parallel_axes_dist,
		'linear_rail_angle': linear_rail_angle,
		'off_axis_joint_position': [off_axis_joint_X, off_axis_joint_Y, off_axis_joint_Z],
		'simDuration': delta_time}

		write2json(jsonFullPath, simdata)
		print(delta_time)
		##########************###########

	except:
		pdb.set_trace()
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



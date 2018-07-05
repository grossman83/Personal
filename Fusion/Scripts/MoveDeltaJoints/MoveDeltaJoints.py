import adsk.core, adsk.fusion, traceback, math, copy
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
jsonFullPath = 'Documents/data23.json'

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
off_axis_z_offset = -1.0 * design.userParameters.itemByName('off_axis_z_offset').value



def getDist2Origin(component):
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
			if joint.jointMotion.rotationValue != thetas[idx]:
				joint.isLocked = False
				joint.jointMotion.rotationValue = thetas[idx]
				joint.isLocked = True
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
		# setRevoluteJoints(revolute_joints, [abs2rev(idx,k) for idx,k in enumerate(thetas)])
		setRevoluteJoints(revolute_joints, [abs2rev(k) for k in thetas])
		# measured_thetas.append([rev2abs(idx, j.jointMotion.rotationValue) for idx,j in enumerate(revolute_joints)])
		measured_thetas.append([rev2abs(j.jointMotion.rotationValue) for j in revolute_joints])

	return desired_thetas, measured_thetas

def sweepJoint_locked(joint_id, revolute_joints, thetas, mobilePlatform):
	try:
		xyzs = []
		angles = []
		revolute_joints[joint_id].isLocked = False
		adsk.doEvents()
		for theta in thetas:
			revolute_joints[joint_id].jointMotion.rotationValue = abs2rev(theta)
			# temp_angles = [rev2abs(idx, j.jointMotion.rotationValue) for idx,j in enumerate(revolute_joints)]
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


def run(context):
	try:
		rootComp = app.activeProduct.rootComponent
		mobilePlatform = rootComp.occurrences.itemByName('Mobile_Platform:1')

		rev0 = rootComp.joints.itemByName('Shoulder0_Revolute')
		rev1 = rootComp.joints.itemByName('Shoulder1_Revolute')
		rev2 = rootComp.joints.itemByName('Shoulder2_Revolute')
		revolute_joints = [rev0, rev1, rev2]


		#revolute_joints = [rootComp.joints.itemByName('Shoulder0_Revolute'), rootComp.joints.itemByName('Shoulder1_Revolute'), rootComp.joints.itemByName('Shoulder2_Revolute')]

		# xyzs = []
		# thetas = []
		xyzs0=[]
		d_xyzs0 = []
		thetas0 = []
		d_thetas0 = []

		xyzs1=[]
		d_xyzs1 = []
		thetas1 = []
		d_thetas1 = []

		xyzs2=[]
		d_xyzs2 = []
		thetas2 = []
		d_thetas2 = []
#		dthetas = []
#		dxyzs = []
		theta_range0 = [10.0*k for k in range(-3,4)]
		theta_range0 = [k*pi/180 for k in theta_range0]

		theta_range1 = [10.0*k for k in range(-3,4)]
		theta_range1 = [k*pi/180 for k in theta_range1]

		theta_range2 = [5.0*k+0.1 for k in range(-15,16)]
		theta_range2 = [k*pi/180 for k in theta_range2]
		dtheta_range2 = [k+0.0001 for k in theta_range2]
		

		loop_count = 0
		start_time = time.time()
		for t0 in theta_range0:
			for t1 in theta_range1:
				setRevoluteJoints(revolute_joints, [t0, t1, theta_range2[0]])
				#perform the sweep
				angles2, sweep_xyzs2 = sweepJoint_locked(2, revolute_joints, theta_range2, mobilePlatform)
				xyzs2.append(sweep_xyzs2)
				# d_xyzs2.append(dsweep_xyzs2)
				thetas2.append(angles2)
				# d_thetas2.append(dangles2)
				# loop_count = loop_count+1
				# print(loop_count/numloops)

		stop_time = time.time()
		delta_time = stop_time - start_time



		##########************###########
		# mydata={'thetas':thetas, 'xyzs':xyzs, 'dthetas':dthetas, 'dxyzs':dxyzs}
		# mydata={
		# 'thetas0':thetas0, 'xyzs0':xyzs0, 'd_thetas0':d_thetas0, 'd_xyzs0':d_xyzs0,
		# 'thetas1':thetas1, 'xyzs1':xyzs1, 'd_thetas1':d_thetas1, 'd_xyzs1':d_xyzs1,
		# 'thetas2':thetas2, 'xyzs2':xyzs2, 'd_thetas2':d_thetas2, 'd_xyzs2':d_xyzs2}
		# mydata={
		# 'thetas0':thetas0, 'xyzs0':xyzs0, 'd_thetas0':d_thetas0, 'd_xyzs0':d_xyzs0}
		mydata = {'xyzs2':xyzs2, 'angles2':angles2}
		write2json(jsonFullPath, mydata)
		print(delta_time)
		##########************###########

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



import adsk.core, adsk.fusion, traceback, math, random
import csv
import os
import json
import time
import operator

pi = math.pi

thetas = []
xyzs = []

rootPath = os.path.expanduser('~')
fullPath = os.path.join(rootPath, 'Documents', 'output3.csv')
jsonFullPath = 'Documents/data10.json'

app = adsk.core.Application.get()
ui = app.userInterface
design = app.activeProduct

# user_joint0_angle = design.userParameters.itemByName('j0_angle')
# user_joint1_angle = design.userParameters.itemByName('j1_angle')
# user_joint2_angle = design.userParameters.itemByName('j2_angle')


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

def setRigidJoints(rigid_joints, revolute_joints, thetas):
	#sets all the joints to the angles(rad) specified in thetas (absolute space)
	#does so by suppressing the rigid joint counterparts to each revolute joint
	#the moves the revolute joint to the specified angle
	#changes the rigid joint angle to match
	#unsuppresses the rigid joint
	#this performs no locking/unlocking of the revolute joints
	try:	
		#set the revolute joints to equal the rigid ones to start things off.
		for idx in range(len(rigid_joints)):
			revolute_joints[idx].jointMotion.rotationValue = rigid2rev(idx, rigid_joints[idx].angle.value)

		for t_idx in zip(thetas, range(len(thetas))):
			theta = t_idx[0]
			idx = t_idx[1]
			# if rigid_joints[idx].angle.value != theta:
			if not math.isclose(rigid_joints[idx].angle.value, abs2rigid(idx, theta), abs_tol = 0.00001):
				#current rigid angle not equal to desired angle... free the joint then drive the revolute
				rigid_joints[idx].isSuppressed = True
				# while not (rigid_joints[idx].isSuppressed):
				# 	time.sleep(0.1)
				adsk.doEvents()
				adsk.doEvents()
				revolute_joints[idx].jointMotion.rotationValue = abs2rev(idx, theta)
				rigid_joints[idx].angle.value = abs2rigid(idx, theta)
				adsk.doEvents()
				rigid_joints[idx].isSuppressed = False
				adsk.doEvents()
				while (rigid_joints[idx].isSuppressed):
					time.sleep(0.1)
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def setRevoluteJoints_locked(revolute_joints, thetas):
	for j_idx in zip(revolute_joints, range(len(thetas))):
		joint = j_idx[0]
		idx = j_idx[1]
		if joint.jointMotion.rotationValue != thetas[idx]:
			joint.isLocked = False
			joint.jointMotion.rotationValue = thetas[idx]
			joint.isLocked = True
			adsk.doEvents()
			adsk.doEvents()
	adsk.doEvents()
	adsk.doEvents()


def rev2rigid(idx, theta):
	try:
		#converts the theta from the revolute space to an equivalent position
		#in the rigid space.
		if idx == 0 or idx == 1:
			return theta + pi/2.0
		if idx == 2:
			return theta
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def rigid2rev(idx, theta):
	try:
		if idx == 0 or idx == 1:
			return theta - pi/2.0
		if idx == 2:
			return theta
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def abs2rigid(idx, theta):
	#60 is all the way up
	#-60 is all the way down
	try:
		if idx == 0 or idx == 1:
			return theta + pi
		if idx == 2:
			return theta + 3.0*pi/2.0
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def rigid2abs(idx, theta):
	try:
		if idx == 0 or idx == 1:
			return theta - pi
		if idx == 2:
			return theta - 3.0*pi/2.0
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def abs2rev(idx, theta):
	try:
		if idx == 0 or idx == 1:
			return theta + pi/2.0
		if idx == 2:
			return theta + 3.0*pi/2.0
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def rev2abs(idx, theta):
	try:
		if idx == 0 or idx == 1:
			return theta - pi/2.0
		if idx == 2:
			return theta - 3.0*pi/2.0
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def sweepJoint(joint_id, rigid_joints, revolute_joints, thetas, mobilePlatform):
	#this holds two joints fixed and uses revolute_joint.jointMotion to drive the joint
	#this is much quicker than locking/unlocking or suppressing/unsuppressing
	try:	
		rigid_joints[joint_id].isSuppressed = True
		xyzs = []
		angles = []
		for theta in thetas:
			revolute_joints[joint_id].jointMotion.rotationValue = abs2rev(joint_id, theta)
			adsk.doEvents()
			temp_angles = [rigid2abs(idx, j.angle.value) for idx, j in enumerate(rigid_joints)]
			temp_angles[joint_id] = theta
			angles.append(temp_angles)
			xyzs.append([mobilePlatform.transform.translation.x, mobilePlatform.transform.translation.y, mobilePlatform.transform.translation.z])
		rigid_joints[joint_id].angle.value = abs2rigid(joint_id, thetas[-1])
		rigid_joints[joint_id].isSuppressed = False
		# while rigid_joints[joint_id].isSuppressed:	
		adsk.doEvents()
		time.sleep(0.1)
		adsk.doEvents()
		return angles, xyzs

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def run(context):
	try:
		rootComp = app.activeProduct.rootComponent
		mobilePlatform = rootComp.occurrences.itemByName('Mobile_Platform:1')
		rigid0 = rootComp.joints.itemByName('Shoulder0')
		rigid1 = rootComp.joints.itemByName('Shoulder1')
		rigid2 = rootComp.joints.itemByName('Shoulder2')
		rev0 = rootComp.joints.itemByName('Shoulder0_Revolute')
		rev1 = rootComp.joints.itemByName('Shoulder1_Revolute')
		rev2 = rootComp.joints.itemByName('Shoulder2_Revolute')
		# user_angles = [design.userParameters.itemByName('j0_angle'), design.userParameters.itemByName('j1_angle'), design.userParameters.itemByName('j2_angle')]

		# rigid_joints = [rigid0, rigid1, rigid2]
#		revolute_joints = [rev0, rev1, rev2]
		rigid_joints = [rootComp.joints.itemByName('Shoulder0'), rootComp.joints.itemByName('Shoulder1'), rootComp.joints.itemByName('Shoulder2')]
		revolute_joints = [rootComp.joints.itemByName('Shoulder0_Revolute'), rootComp.joints.itemByName('Shoulder1_Revolute'), rootComp.joints.itemByName('Shoulder2_Revolute')]

		dtheta = 0.1*pi/180.0#0.1degree

		xyzs = []
		thetas = []
		dthetas = []
		dxyzs = []
		theta_range0 = [10.0*k for k in range(-1,1)]
		theta_range0 = [k*pi/180 for k in theta_range0]

		theta_range1 = [10.0*k for k in range(-1,1)]
		theta_range1 = [k*pi/180 for k in theta_range1]

		theta_range2 = [3.0*k for k in range(-10,11)]
		theta_range2 = [k*pi/180 for k in theta_range2]
		start_time = time.time()


		loop_count = 0
		for t0 in theta_range0:
			for t1 in theta_range1:
				setRigidJoints(rigid_joints, revolute_joints, [t0, t1, theta_range2[0]])
				#perform the sweep
				angles, sweep_xyzs = sweepJoint(2, rigid_joints, revolute_joints, theta_range2, mobilePlatform)
				xyzs.append(sweep_xyzs)
				thetas.append(angles)
				# loop_count = loop_count+1
				# print(loop_count/numloops)
		stop_time = time.time()
		delta_time = stop_time - start_time




		##########************###########
		# mydata={'thetas':thetas, 'xyzs':xyzs, 'dthetas':dthetas, 'dxyzs':dxyzs}
		mydata={'thetas':thetas, 'xyzs':xyzs}
		write2json(jsonFullPath, mydata)
		print(delta_time)
		##########************###########

#		forCSV = [xyzs, dxyzs, dthetas]

#		write2CSV(thetas, fullPath)

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



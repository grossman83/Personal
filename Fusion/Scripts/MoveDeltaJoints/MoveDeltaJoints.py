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
jsonFullPath = 'Documents/data7.json'

app = adsk.core.Application.get()
ui = app.userInterface
design = app.activeProduct

user_joint0_angle = design.userParameters.itemByName('j0_angle')
user_joint1_angle = design.userParameters.itemByName('j1_angle')
user_joint2_angle = design.userParameters.itemByName('j2_angle')


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
	#sets all the joints to the angles(rad) specified in thetas
	#does so by suppressing the rigid joint counterparts to each revolute joint
	#the moves the revolute joint to the specified angle
	#changes the rigid joint angle to match
	#unsuppresses the rigid joint
	#this performs no locking/unlocking of the revolute joints
	try:	
		for t_idx in zip(thetas, range(len(thetas))):
			theta = t_idx[0]
			idx = t_idx[1]
			if rigid_joints[idx].angle.value != theta:
				#current rigid angle not equal to desired angle... free the joint then move as revolute
				rigid_joints[idx].isSuppressed = True
				revolute_joints[idx].jointMotion.rotationValue = theta
				#now set the user angle that defines the rigid joint to match
				# user_angle.value = thetas[idx]
				# adsk.doEvents()
				rigid_joints[idx].angle.value = theta
				rigid_joints[idx].isSuppressed = False
				adsk.doEvents()
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

def sweepJoint(joint_id, rigid_joints, revolute_joints, thetas, mobilePlatform):
	#this holds two joints fixed and uses revolute_joint.jointMotion to drive the joint
	#this is much quicker than locking/unlocking or suppressing/unsuppressing
	try:	
		rigid_joints[joint_id].isSuppressed = True
		xyzs = []
		angles = []
		for theta in thetas:
			revolute_joints[joint_id].jointMotion.rotationValue = theta
			adsk.doEvents()
			temp_angles = [j.angle.value for j in rigid_joints]
			temp_angles[joint_id] = theta
			angles.append(temp_angles)
			xyzs.append([mobilePlatform.transform.translation.x, mobilePlatform.transform.translation.y, mobilePlatform.transform.translation.z])
		rigid_joints[joint_id].angle.value = thetas[-1]
		rigid_joints[joint_id].isSuppressed = False
		adsk.doEvents()
		time.sleep(0.2)
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
		joint0_rev = rootComp.joints.itemByName('Shoulder0_Revolute')
		joint1_rev = rootComp.joints.itemByName('Shoulder1_Revolute')
		joint2_rev = rootComp.joints.itemByName('Shoulder2_Revolute')
		# user_angles = [design.userParameters.itemByName('j0_angle'), design.userParameters.itemByName('j1_angle'), design.userParameters.itemByName('j2_angle')]

		rigid_joints = [rigid0, rigid1, rigid2]
		revolute_joints = [joint0_rev, joint1_rev, joint2_rev]

		dtheta = 0.1*pi/180.0#0.1degree

		xyzs = []
		thetas = []
		dthetas = []
		dxyzs = []
		theta_range0 = [10.0*k for k in range(-3,4)]
		theta_range1 = [10.0*k for k in range(-3,4)]
		theta_range1.reverse()
		theta_range2 = [3.0*k*pi/180.0 for k in range(-20,21)]
		start_time = time.time()


		for t0 in theta_range0:
			for t1 in theta_range1:
				#set the angles
				t0 = t0/180.0*pi
				t1 = t1/180.0*pi
				setRigidJoints(rigid_joints, revolute_joints, [t0, t1, theta_range2[0]])
				#perform the sweep
				angles, sweep_xyzs = sweepJoint(2, rigid_joints, revolute_joints, theta_range2, mobilePlatform)
				xyzs.append(sweep_xyzs)
				thetas.append(angles)
				

				#now move by dtheta in each axis
				# setRigidJoints(rigid_joints, revolute_joints, user_angles, [t0+dtheta, t1+dtheta, t2+dtheta])
				# setRevoluteJoints_locked(revolute_joints, [t0+dtheta, t1+dtheta, t2+dtheta])
				# nxyzs = [mobilePlatform.transform.translation.x, mobilePlatform.transform.translation.y, mobilePlatform.transform.translation.x]
				# dxyzs.append(list(map(operator.sub, nxyzs, cur_xyzs)))
				# dthetas.append(dtheta)



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



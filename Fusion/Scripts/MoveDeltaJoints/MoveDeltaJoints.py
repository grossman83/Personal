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

user_joint_angles = [user_joint0_angle, user_joint1_angle, user_joint2_angle]

#NOT WORKING
# class myRigidJoint:
# 	def __init__(self, fusion_joint_object, user_joint_angle):
# 		self.fjo = fusion_joint_object
# 		self.user_angle = user_joint_angle.value
# 		self.suppressed = self.fjo.isSuppressed
#NOT WORKING


def getDist2Origin(component):
	try:
		trans = component.transform.translation
		return [trans.x,trans.y,trans.z]
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
	
# Get health state of a joint
# health = joint.healthState
# if health == adsk.fusion.FeatureHealthStates.ErrorFeatureHealthState or health == adsk.fusion.FeatureHealthStates.WarningFeatureHealthState:
#     message = joint.errorOrWarningMessage



def moveJoint(free_joint, fixed_joints, newAngle):
	try:
		revoluteMotion = adsk.fusion.RevoluteJointMotion.cast(free_joint.jointMotion)
		for j in fixed_joints:
			if not (j.isLocked):
				j._set_isLocked(True)
		revoluteMotion.rotationValue = pi*newAngle/180.0
		adsk.doEvents()
		#unlock the joints
		for j in fixed_joints:
			if j.isLocked:
				j._set_isLocked(False)
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def write2CSV(list_of_lists, filepath):
	try:
		with open(fullPath, 'w', newline='\n') as f:
			writer = csv.writer(f)
			for val in list_of_lists:
				writer.writerow(val)
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def readCSV(fullPath):
	blah = []
	with open(fullPath) as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			blah.append(row)

	csvfile.close()
	return blah

def write2json(filePath, data):
	with open(filePath, 'w') as fp:
		# json.dump(data, fp)
		json.dump(data, fp, sort_keys=True, indent=4, separators=(',', ': '))

def setRigidJoints2(rigid_joints, revolute_joints, thetas):
	try:	
		# user_angles = [j.user_angle for j in rigid_joints]
		for ua_idx in zip(thetas, range(len(thetas))):
			theta = ua_idx[0]
			idx = ua_idx[1]
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

def setRigidJoints(rigid_joints, revolute_joints, user_angles, thetas):
	try:	
		for ua_idx in zip(user_angles, range(len(thetas))):
			user_angle = ua_idx[0]
			idx = ua_idx[1]
			if user_angle.value != thetas[idx]:
				#current rigid angle not equal to desired angle... free the joint then move as revolute
				revolute_joints[idx].jointMotion.rotationValue = thetas[idx]
				#now set the user angle that defines the rigid joint to match
				user_angles[idx].value = thetas[idx]
				rigid_joints[idx].isSuppressed = True
				rigid_joints[idx].isSuppressed = False
		adsk.doEvents()
		adsk.doEvents()
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def quickSetRigidJoints(rigid_joints, revolute_joints, thetas):
	try:	
		for idx in range(len(thetas)):
			current_angle = rigid_joints[idx].angle.value
			if current_angle != thetas[idx]:
				#current rigid angle not equal to desired angle
				# revolute_joints[idx].jointMotion.rotationValue = thetas[idx]
				rigid_joints[idx].angle.value = thetas[idx]
		adsk.doEvents()
		adsk.doEvents()
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



def setRevoluteJoints(rigid_joints, revolute_joints, thetas):
	for j_idx in zip(rigid_joints, range(len(thetas))):
		j = j_idx[0]
		idx = j_idx[1]
		j.isSuppressed = True
		j.angle.value = thetas[idx]
	for j_idx in zip(revolute_joints, range(len(thetas))):
		j = j_idx[0]
		idx = j_idx[1]
		j.jointMotion.rotationValue = thetas[idx]
	for j in rigid_joints:
		j.isSuppressed = False
		adsk.doEvents()

def setRevoluteJoints2(rigid_joints, revolute_joints, thetas):
	for j in rigid_joints:
		if not j.isSuppressed:
			j.isSuppressed = True
	for j_idx in zip(revolute_joints, range(len(thetas))):
		j_idx[0].jointMotion.rotationValue = thetas[j_idx[1]]


def suppressJoints(joints):
	for j in joints:
		j.isSuppressed = True
		while not j.isSuppressed:
			time.sleep(0.05)
		# adsk.doEvents()

def unSuppressJoints(joints):
	for j in joints:
		j.isSuppressed = False
		while j.isSuppressed:
			time.sleep(0.05)
		# adsk.doEvents()

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



# def setRevoluteJoints(rigid_joints, revolute_joints, thetas):
# 	for j_idx in zip(rigid_joints, range(len(thetas))):
# 		j = j_idx[0]
# 		idx = j_idx[1]
# 		j.isSuppressed = True
# 		j.angle.value = thetas[idx]
# 	for j_idx in zip(revolute_joints, range(len(thetas))):
# 		j = j_idx[0]
# 		idx = j_idx[1]
# 		j.jointMotion.rotationValue = thetas[idx]
# 	for j in rigid_joints:
# 		j.isSuppressed = False
# 		adsk.doEvents()



# sweepJoint2(0, rigid_joints, revolute_joints, [k*pi/180 for k in range(-50,50)], mobilePlatform)
def sweepJoint2(joint_id, rigid_joints, revolute_joints, thetas, mobilePlatform):
	try:	
		rigid_joints[joint_id].isSuppressed = True
		xyzs = []
		angles = []
		for theta in thetas:
			revolute_joints[joint_id].jointMotion.rotationValue = theta
			adsk.doEvents()
			# temp_angles = [j.user_angle for j in rigid_joints]
			temp_angles = [j.angle.value for j in rigid_joints]
			temp_angles[joint_id] = theta
			angles.append(temp_angles)
			xyzs.append([mobilePlatform.transform.translation.x, mobilePlatform.transform.translation.y, mobilePlatform.transform.translation.z])
		rigid_joints[joint_id].user_angle = thetas[-1]
		rigid_joints[joint_id].isSuppressed = False
		adsk.doEvents()
		return angles, xyzs

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def testSuppress(rigid_joints):
	try:
		for j in rigid_joints:
			j.isSuppressed = True
			j.isSuppressed = False
		adsk.doEvents()
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def run(context):
	try:
		rootComp = app.activeProduct.rootComponent

		mobilePlatform = rootComp.occurrences.itemByName('Mobile_Platform:1')

		#NOT Working
		# rigid0 = myRigidJoint(rootComp.joints.itemByName('Shoulder0'), design.userParameters.itemByName('j0_angle'))
		# rigid1 = myRigidJoint(rootComp.joints.itemByName('Shoulder1'), design.userParameters.itemByName('j1_angle'))
		# rigid2 = myRigidJoint(rootComp.joints.itemByName('Shoulder2'), design.userParameters.itemByName('j2_angle'))
		# my_rigid_joints = [rigid0, rigid1, rigid2]
		#NOT Working
		



		rigid0 = rootComp.joints.itemByName('Shoulder0')
		rigid1 = rootComp.joints.itemByName('Shoulder1')
		rigid2 = rootComp.joints.itemByName('Shoulder2')

		user_angles = [design.userParameters.itemByName('j0_angle'), design.userParameters.itemByName('j1_angle'), design.userParameters.itemByName('j2_angle')]

		joint0_rev = rootComp.joints.itemByName('Shoulder0_Revolute')
		joint1_rev = rootComp.joints.itemByName('Shoulder1_Revolute')
		joint2_rev = rootComp.joints.itemByName('Shoulder2_Revolute')

		rigid_joints = [rigid0, rigid1, rigid2]
		revolute_joints = [joint0_rev, joint1_rev, joint2_rev]

		dtheta = 0.1*pi/180.0#0.1degree

		xyzs = []
		thetas = []
		dthetas = []
		dxyzs = []
		theta_range = [5*k for k in range(-10,11)]
		start_time = time.time()
		for t0 in theta_range:
			for t1 in theta_range:
				for t2 in theta_range:
					#set the angles
					t0 = t0/180.0*pi
					t1 = t1/180.0*pi
					t2 = t2/180.0*pi
					# setRigidJoints2(rigid_joints, revolute_joints, user_angles, [t0, t1, t2])
					setRevoluteJoints_locked(revolute_joints, [t0,t1,t1])
					#calc mobile platform position
					cur_xyzs = [mobilePlatform.transform.translation.x, mobilePlatform.transform.translation.y, mobilePlatform.transform.translation.x]
					xyzs.append(cur_xyzs)
					thetas.append([t0, t1, t2])
					#now move by dtheta in each axis
					# setRigidJoints2(rigid_joints, revolute_joints, user_angles, [t0+dtheta, t1+dtheta, t2+dtheta])
					setRevoluteJoints_locked(revolute_joints, [t0+dtheta, t1+dtheta, t2+dtheta])
					nxyzs = [mobilePlatform.transform.translation.x, mobilePlatform.transform.translation.y, mobilePlatform.transform.translation.x]
					dxyzs.append(list(map(operator.sub, nxyzs, cur_xyzs)))
					dthetas.append(dtheta)



		stop_time = time.time()
		delta_time = stop_time - start_time

		###########TEST###########
		# start_time = time.time()
		# test_len = 101
		# for k in range(test_len):
		# 	testSuppress(rigid_joints)
		# stop_time = time.time()
		# delta_time = stop_time-start_time
		###########TEST###########





		###########TEST###########
		# test_len = 100
		# thetas = [[pi*random.randint(-50,50)/180.0, pi*random.randint(-50,50)/180.0, pi*random.randint(-50,50)/180.0 ] for k in range(test_len)]
		# start_time = time.time()
		# for vals in thetas:
		# 	# setRigidJoints3(rigid_joints, revolute_joints, user_angles, vals)
		# 	setRevoluteJoints_locked(revolute_joints, vals)
		# stop_time = time.time()

		# delta_time = stop_time-start_time
		###########TEST###########

		###########TEST###########
		# test_len = 100
		# thetas = [[pi*random.randint(-50,50)/180.0, pi*random.randint(-50,50)/180.0, pi*random.randint(-50,50)/180.0 ] for k in range(test_len)]
		# start_time = time.time()
		# for vals in thetas:
		# 	testSuppress(rigid_joints)
		# stop_time = time.time()

		# delta_time = stop_time-start_time
		###########TEST###########




		###########TEST###########
		# start_time = time.time()
		# thetas, xyzs = sweepJoint(0, rigid_joints, rev_joints, [k*pi/180 for k in range(-50,50)], mobilePlatform)
		# stop_time = time.time()
		###########TEST###########


		##########************###########
		mydata={'thetas':thetas, 'xyzs':xyzs, 'dthetas':dthetas, 'dxyzs':dxyzs}
		write2json(jsonFullPath, mydata)
		print(delta_time)
		##########************###########

#		forCSV = [xyzs, dxyzs, dthetas]

#		write2CSV(thetas, fullPath)

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
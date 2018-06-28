import adsk.core, adsk.fusion, traceback, math, random
import csv
import os
import time

pi = math.pi

thetas = []
xyzs = []

rootPath = os.path.expanduser('~')
fullPath = os.path.join(rootPath, 'Documents', 'output3.csv')

app = adsk.core.Application.get()
ui = app.userInterface
design = app.activeProduct

user_joint0_angle = design.userParameters.itemByName('joint0_angle')
user_joint1_angle = design.userParameters.itemByName('joint1_angle')
user_joint2_angle = design.userParameters.itemByName('joint2_angle')

user_joint_angles = [user_joint0_angle, user_joint1_angle, user_joint2_angle]


class myRigidJoint:
	def __init__(self, fusion_joint_object, user_joint_angle):
		self.fjo = fusion_joint_object
		self.user_angle = user_joint_angle.value
		self.suppressed = fusion_joint_object.isSuppressed
		# self.corresponding_revolute_name = corresponding_revolute_name

# class myRevoluteJoint(fusion_joint_object, corresponding_rigid_name):
# 	def __init__:
# 		self.corresponding_rigid_name = corresponding_rigid_name




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


# def move2thetas(rigid_joints, revolute_joints, new_thetas):
# 	current_thetas = [k.angle.value for k in rigid_joints]
# 	for k in zip(current_thetas, new_thetas):
# 		if k[0] != k[1]:



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



# def setRigidJoints(rigid_joints, thetas):
# 	# user_joint0_angle.value = thetas[0]*pi/180
# 	# user_joint1_angle.value = thetas[1]*pi/180
# 	# user_joint2_angle.value = thetas[2]*pi/180
# 	for tr in zip(rigid_joints, thetas):
# 		tr[0].user_angle = tr[1]
# 	adsk.doEvents()


def setRigidJoints(rigid_joints, revolute_joints, thetas):
	current_thetas = [j.user_angle for j in rigid_joints]
	for Ts in zip(current_thetas, range(len(thetas))):
		if Ts[0] != thetas[Ts[1]]:
			#current rigid angle not equal to desired angle... free the joint then move as revolute
			rigid_joints[Ts[1]].isSuppressed = True
			revolute_joints[Ts[1]].jointMotion.rotationValue = thetas[0]
			#now set the user angle that defines the rigid joint to match
			rigid_joints[Ts[1]].user_angle = thetas[0]
			rigid_joints[Ts[1]].isSuppressed = False
			adsk.doEvents()



def sweepJoint(joint_id, rigid_joints, revolute_joints, thetas, mobilePlatform):
	rigid_joints[joint_id].isSuppressed = True
	xyzs = []
	angles = []
	for theta in thetas:
		revolute_joints[joint_id].jointMotion.rotationValue = theta
		adsk.doEvents()
		temp_angles = [j.user_angle for j in rigid_joints]
		temp_angles[joint_id] = theta
		angles.append(temp_angles)
		xyzs.append([mobilePlatform.transform.translation.x, mobilePlatform.transform.translation.y, mobilePlatform.transform.translation.z])
	rigid_joints[joint_id].user_angle = thetas[-1]
	rigid_joints[joint_id].isSuppressed = False
	adsk.doEvents()
	return angles, xyzs

	

def exploreLocation(rigid_joints, rev_joints):
	#supporess one rigid joint then explore dtheta/ddist in both directions around that point
	#the repeat for the other two joints
	dthetas
	dtheta = 0.0001#rad
	for rj in zip(rigid_joints, list(range(3))):
		rj[0].isSuppressed = True
		rev_joints[rj[1]].jointMotion.rotationValue = user_joint_angles[rj[1]] + dtheta



def run(context):
	try:
		rootComp = app.activeProduct.rootComponent

		mobilePlatform = rootComp.occurrences.itemByName('Mobile_Platform:1')

		rigid0 = myRigidJoint(rootComp.joints.itemByName('Shoulder0'), design.userParameters.itemByName('joint0_angle'))
		rigid1 = myRigidJoint(rootComp.joints.itemByName('Shoulder1'), design.userParameters.itemByName('joint1_angle'))
		rigid2 = myRigidJoint(rootComp.joints.itemByName('Shoulder2'), design.userParameters.itemByName('joint1_angle'))

		joint0_rev = rootComp.joints.itemByName('Shoulder0_Revolute')
		joint1_rev = rootComp.joints.itemByName('Shoulder1_Revolute')
		joint2_rev = rootComp.joints.itemByName('Shoulder2_Revolute')

		rigid_joints = [rigid0, rigid1, rigid2]
		rev_joints = [joint0_rev, joint1_rev, joint2_rev]

		# test_len = 100
		# thetas = [[pi*random.randint(-50,50)/180.0, pi*random.randint(-50,50)/180.0, pi*random.randint(-50,50)/180.0 ] for k in range(test_len)]
		# start_time = time.time()
		# for vals in thetas:
		# 	setRigidJoints(rigid_joints, rev_joints, vals)
		# stop_time = time.time()

		# delta_time = stop_time-start_time




		start_time = time.time()
		thetas, xyzs = sweepJoint(0, rigid_joints, rev_joints, [k*pi/180 for k in range(-50,50)], mobilePlatform)
		stop_time = time.time()



		write2CSV(thetas, fullPath)

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
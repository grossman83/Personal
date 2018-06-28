import adsk.core, adsk.fusion, traceback, math
import csv
import os
import time

pi = math.pi

thetas = []
xyzs = []

rootPath = os.path.expanduser('~')
fullPath = os.path.join(rootPath, 'Documents', 'output5.csv')

app = adsk.core.Application.get()
ui = app.userInterface
design = app.activeProduct

user_joint0_angle = design.userParameters.itemByName('joint0_angle')
user_joint1_angle = design.userParameters.itemByName('joint1_angle')
user_joint2_angle = design.userParameters.itemByName('joint2_angle')


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



def setRigidJoints(thetas):
	user_joint0_angle.value = thetas[0]*pi/180
	user_joint1_angle.value = thetas[1]*pi/180
	user_joint2_angle.value = thetas[2]*pi/180
	adsk.doEvents()
	


def run(context):
	try:
		rootComp = app.activeProduct.rootComponent

		mobilePlatform = rootComp.occurrences.itemByName('Mobile_Platform:1')

		joint0 = rootComp.joints.itemByName('Shoulder0')
		joint1 = rootComp.joints.itemByName('Shoulder1')
		joint2 = rootComp.joints.itemByName('Shoulder2')

		joint0_rev = rootComp.joints.itemByName('Shoulder0_Revolute')
		joint1_rev = rootComp.joints.itemByName('Shoulder1_Revolute')
		joint2_rev = rootComp.joints.itemByName('Shoulder2_Revolute')

		joint0_
#		start_time = time.time()
		for t1 in range(-50,50):
			for t2 in range(-50,50):
				for t3 in range(-50,50):
					setRigidJoints([t1,t2,t3])
					dists = getDist2Origin(mobilePlatform)
					theta0 = joint0.angle.value*180/pi
					theta1 = joint1.angle.value*180/pi
					theta2 = joint2.angle.value*180/pi
					thetas.append([[theta0, theta1, theta2], dists])
#					loop_time = time.time()-start_time
#					print(loop_time)

		write2CSV(thetas, fullPath)

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
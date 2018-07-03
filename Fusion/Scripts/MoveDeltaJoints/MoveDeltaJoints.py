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
jsonFullPath = 'Documents/data20.json'

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


#[k*180/pi for k in thetas]
#[rev2abs(idx, k.jointMotion.rotationValue)*180/pi for idx, k in enumerate(revolute_joints)]
#[rigid2abs(idx, k.angle.value)*180/pi for idx, k in enumerate(rigid_joints)]





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
			adsk.doEvents()



		# for t_idx in zip(thetas, range(len(thetas))):
		for idx, theta in enumerate(thetas):
			if not math.isclose(rigid_joints[idx].angle.value, abs2rigid(idx, theta), abs_tol = 0.00001):
				#current rigid angle not equal to desired angle... free the joint then drive the revolute
				rigid_joints[idx].isSuppressed = True
				current_theta = revolute_joints[idx].jointMotion.rotationValue
				desired_theta = abs2rev(idx, theta)
				positive_move = (desired_theta > current_theta)
				step_size = 10.0/180.0*pi
				numsteps = math.ceil(abs(desired_theta - current_theta)/(step_size))
				if numsteps > 1:
					if positive_move:
						#create list of positions to step through
						step_thetas = [k*step_size + current_theta for k in range(numsteps)]
						for stp in step_thetas:
							revolute_joints[idx].jointMotion.rotationValue = stp
							adsk.doEvents()
					else:#negative move
						step_thetas = [-1.0*k*step_size + current_theta for k in range(numsteps)]
						for stp in step_thetas:
							revolute_joints[idx].jointMotion.rotationValue = stp
							adsk.doEvents()
				
				#finish the move with one final step since range doesn't got to endpoint
				revolute_joints[idx].jointMotion.rotationValue = abs2rev(idx, theta)
				adsk.doEvents()
				rigid_joints[idx].angle.value = abs2rigid(idx, theta)
				adsk.doEvents()
				rigid_joints[idx].isSuppressed = False
				adsk.doEvents()
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def setRevoluteJoints_locked(revolute_joints, thetas):
	#successively unlocks, then moves any joint that is not set to the angle desired by thetas
	#NOTES:
	#did not work correctly without both adsk.doEvents() commands at the end
	#does appear to work with the doEvents() after locking and unlocking commented out
	for idx, joint in enumerate(revolute_joints):
		if joint.jointMotion.rotationValue != thetas[idx]:
			joint.isLocked = False
			# adsk.doEvents()
			joint.jointMotion.rotationValue = thetas[idx]
			# adsk.doEvents()
			joint.isLocked = True
			# adsk.doEvents()
	adsk.doEvents()
	adsk.doEvents()

#test script
# desired_thetas, measured_thetas = test_setRevoluteJoints_locked(revolute_joints)
# [list(map(operator.sub, k[0],k[1])) for k in zip(desired_thetas, measured_thetas)]
def test_setRevoluteJoints_locked(revolute_joints):
	#move randomly between -60, and 60
	desired_thetas = []
	measured_thetas = []
	for k in range(60):
		rand_angles = [random.randint(-60,60) for k in range(3)]
		thetas = [k*pi/180 for k in rand_angles]
		desired_thetas.append(thetas)
		setRevoluteJoints_locked(revolute_joints, [abs2rev(idx,k) for idx,k in enumerate(thetas)])
		measured_thetas.append([rev2abs(idx, j.jointMotion.rotationValue) for idx,j in enumerate(revolute_joints)])

	return desired_thetas, measured_thetas




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
		adsk.doEvents()
		xyzs = []
		angles = []
		for theta in thetas:
			revolute_joints[joint_id].jointMotion.rotationValue = abs2rev(joint_id, theta)
			adsk.doEvents()
			temp_angles = [rigid2abs(idx, j.angle.value) for idx, j in enumerate(rigid_joints)]
			temp_angles[joint_id] = theta
			angles.append(temp_angles)
			xyzs.append([mobilePlatform.transform.translation.x, mobilePlatform.transform.translation.y, mobilePlatform.transform.translation.z])
		#gently sweep things back so as to help solve
		thetas.reverse()
		for theta in thetas:
			revolute_joints[joint_id].jointMotion.rotationValue = abs2rev(joint_id, theta)
			adsk.doEvents()
		rigid_joints[joint_id].angle.value = abs2rigid(joint_id, thetas[-1])
		adsk.doEvents()
		rigid_joints[joint_id].isSuppressed = False
		adsk.doEvents()
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

		rigid_joints = [rigid0, rigid1, rigid2]
		revolute_joints = [rev0, rev1, rev2]
#		rigid_joints = [rootComp.joints.itemByName('Shoulder0'), rootComp.joints.itemByName('Shoulder1'), rootComp.joints.itemByName('Shoulder2')]
#		revolute_joints = [rootComp.joints.itemByName('Shoulder0_Revolute'), rootComp.joints.itemByName('Shoulder1_Revolute'), rootComp.joints.itemByName('Shoulder2_Revolute')]

#		dtheta = 0.1*pi/180.0#0.1degree

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
		theta_range0 = [10.0*k for k in range(-6,7)]
		theta_range0 = [k*pi/180 for k in theta_range0]

		theta_range1 = [10.0*k for k in range(-6,7)]
		theta_range1 = [k*pi/180 for k in theta_range1]

		theta_range2 = [3.0*k for k in range(-10,11)]
		theta_range2 = [k*pi/180 for k in theta_range2]
		dtheta_range2 = [k+0.0001 for k in theta_range2]
		start_time = time.time()


		loop_count = 0
		for t0 in theta_range0:
			for t1 in theta_range1:
				setRigidJoints(rigid_joints, revolute_joints, [t0, t1, theta_range2[0]])
				#perform the sweep
				angles2, sweep_xyzs2 = sweepJoint(2, rigid_joints, revolute_joints, copy.copy(theta_range2), mobilePlatform)
				dangles2, dsweep_xyzs2 = sweepJoint(2, rigid_joints, revolute_joints, copy.copy(dtheta_range2), mobilePlatform)
				xyzs2.append(sweep_xyzs2)
				d_xyzs2.append(dsweep_xyzs2)
				thetas2.append(angles2)
				d_thetas2.append(dangles2)
				# loop_count = loop_count+1
				# print(loop_count/numloops)
		
		# for t0 in theta_range0:
		# 	for t1 in theta_range1:
		# 		setRigidJoints(rigid_joints, revolute_joints, [theta_range2[0], t0, t1])
		# 		#perform the sweep
		# 		angles0, sweep_xyzs0 = sweepJoint(0, rigid_joints, revolute_joints, copy.copy(theta_range2), mobilePlatform)
		# 		dangles0, dsweep_xyzs0 = sweepJoint(0, rigid_joints, revolute_joints, copy.copy(dtheta_range2), mobilePlatform)
		# 		xyzs0.append(sweep_xyzs0)
		# 		d_xyzs0.append(dsweep_xyzs0)
		# 		thetas0.append(angles0)
		# 		d_thetas0.append(dangles0)


		# for t0 in theta_range0:
		# 	for t1 in theta_range1:
		# 		setRigidJoints(rigid_joints, revolute_joints, [t1, theta_range2[0], t0])
		# 		#perform the sweep
		# 		angles1, sweep_xyzs1 = sweepJoint(1, rigid_joints, revolute_joints, copy.copy(theta_range2), mobilePlatform)
		# 		dangles1, dsweep_xyzs1 = sweepJoint(1, rigid_joints, revolute_joints, copy.copy(dtheta_range2), mobilePlatform)
		# 		xyzs1.append(sweep_xyzs1)
		# 		d_xyzs1.append(dsweep_xyzs1)
		# 		thetas1.append(angles1)
		# 		d_thetas1.append(dangles1)





		stop_time = time.time()
		delta_time = stop_time - start_time




		##########************###########
		# mydata={'thetas':thetas, 'xyzs':xyzs, 'dthetas':dthetas, 'dxyzs':dxyzs}
		# mydata={
		# 'thetas0':thetas0, 'xyzs0':xyzs0, 'd_thetas0':d_thetas0, 'd_xyzs0':d_xyzs0,
		# 'thetas1':thetas1, 'xyzs1':xyzs1, 'd_thetas1':d_thetas1, 'd_xyzs1':d_xyzs1,
		# 'thetas2':thetas2, 'xyzs2':xyzs2, 'd_thetas2':d_thetas2, 'd_xyzs2':d_xyzs2}
		mydata={
		'thetas0':thetas0, 'xyzs0':xyzs0, 'd_thetas0':d_thetas0, 'd_xyzs0':d_xyzs0}
		write2json(jsonFullPath, mydata)
		print(delta_time)
		##########************###########

#		forCSV = [xyzs, dxyzs, dthetas]

#		write2CSV(thetas, fullPath)

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



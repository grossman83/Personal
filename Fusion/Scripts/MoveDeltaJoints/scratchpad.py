
#NOT WORKING
# class myRigidJoint:
# 	def __init__(self, fusion_joint_object, user_joint_angle):
# 		self.fjo = fusion_joint_object
# 		self.user_angle = user_joint_angle.value
# 		self.suppressed = self.fjo.isSuppressed
#NOT WORKING


###########TEST###########
# start_time = time.time()
# test_len = 101
# for k in range(test_len):
# 	testSuppress(rigid_joints)
# stop_time = time.time()
# delta_time = stop_time-start_time
###########TEST###########


##########TEST##############
		# start_time = time.time()
		# test_setRevoluteJoints_locked(revolute_joints)
		# stop_time = time.time()
		# run_time = stop_time - start_time
##########TEST##############




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



#NOT Working
# rigid0 = myRigidJoint(rootComp.joints.itemByName('Shoulder0'), design.userParameters.itemByName('j0_angle'))
# rigid1 = myRigidJoint(rootComp.joints.itemByName('Shoulder1'), design.userParameters.itemByName('j1_angle'))
# rigid2 = myRigidJoint(rootComp.joints.itemByName('Shoulder2'), design.userParameters.itemByName('j2_angle'))
# my_rigid_joints = [rigid0, rigid1, rigid2]
#NOT Working


###########TEST###########
# start_time = time.time()
# thetas, xyzs = sweepJoint(0, rigid_joints, rev_joints, [k*pi/180 for k in range(-50,50)], mobilePlatform)
# stop_time = time.time()
###########TEST###########



# Get health state of a joint
# health = joint.healthState
# if health == adsk.fusion.FeatureHealthStates.ErrorFeatureHealthState or health == adsk.fusion.FeatureHealthStates.WarningFeatureHealthState:
#     message = joint.errorOrWarningMessage



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




def setRevoluteJoints2(rigid_joints, revolute_joints, thetas):
	for j in rigid_joints:
		if not j.isSuppressed:
			j.isSuppressed = True
	for j_idx in zip(revolute_joints, range(len(thetas))):
		j_idx[0].jointMotion.rotationValue = thetas[j_idx[1]]

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


def testSuppress(rigid_joints):
	try:
		for j in rigid_joints:
			j.isSuppressed = True
			j.isSuppressed = False
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




		# for t0 in theta_range:
		# 	for t1 in theta_range:
		# 		for t2 in theta_range:
		# 			#set the angles
		# 			t0 = t0/180.0*pi
		# 			t1 = t1/180.0*pi
		# 			t2 = t2/180.0*pi
		# 			# setRigidJoints(rigid_joints, revolute_joints, user_angles, [t0, t1, t2])
		# 			setRevoluteJoints_locked(revolute_joints, [t0,t1,t1])
		# 			#calc mobile platform position
		# 			cur_xyzs = [mobilePlatform.transform.translation.x, mobilePlatform.transform.translation.y, mobilePlatform.transform.translation.x]
		# 			xyzs.append(cur_xyzs)
		# 			thetas.append([t0, t1, t2])
		# 			#now move by dtheta in each axis
		# 			# setRigidJoints(rigid_joints, revolute_joints, user_angles, [t0+dtheta, t1+dtheta, t2+dtheta])
		# 			setRevoluteJoints_locked(revolute_joints, [t0+dtheta, t1+dtheta, t2+dtheta])
		# 			nxyzs = [mobilePlatform.transform.translation.x, mobilePlatform.transform.translation.y, mobilePlatform.transform.translation.x]
		# 			dxyzs.append(list(map(operator.sub, nxyzs, cur_xyzs)))
		# 			dthetas.append(dtheta)
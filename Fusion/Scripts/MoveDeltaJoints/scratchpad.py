
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



[rev2abs(idx, k.jointMotion.rotationValue)*180/pi for idx, k in enumerate(revolute_joints)]
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


# user_joint0_angle = design.userParameters.itemByName('j0_angle')
# user_joint1_angle = design.userParameters.itemByName('j1_angle')
# user_joint2_angle = design.userParameters.itemByName('j2_angle')
# rigid_X = design.userParameters.itemByName('RJ_X')
# rigid_Y = design.userParameters.itemByName('RJ_Y')
# rigid_Z = design.userParameters.itemByName('RJ_Z')





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
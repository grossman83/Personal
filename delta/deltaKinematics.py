#delta robot kinematics

import numpy as np
import marcmath

import pdb


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



def rotateAboutAxis(axisUnitVector, point, theta):
	uV = axisUnitVector
	#R from wikipedia rotation about unit vector
	R = [[np.cos(theta) + uV[0]**2 * (1-np.cos(theta)), uV[0]*uV[1]*(1-np.cos(theta)) - uV[2]*np.sin(theta), uV[0]*uV[2]*(1-np.cos(theta))+uV[1]*np.sin(theta)], [uV[1]*uV[0]*(1-np.cos(theta))+uV[2]*np.sin(theta), np.cos(theta)+uV[1]**2 * (1-np.cos(theta)), uV[1]*uV[2]*(1-np.cos(theta))-uV[0]*np.sin(theta)], [uV[2]*uV[0]*(1-np.cos(theta)) - uV[1]*np.sin(theta), uV[2]*uV[1]*(1-np.cos(theta))+uV[0]*np.sin(theta), np.cos(theta)+uV[2]**2 * (1-np.cos(theta))]]
	return np.dot(R, point)


class createDR(object):
	def __init__(self, L, l, sB, sP):
		self.L = L
		self.l = l
		self.sB = sB
		self.sP = sP

		self.wB = np.sqrt(3)/6*sB
		self.uB = np.sqrt(3)/3*sB

		#Fixed platform connection points
		self.BB1 = [0, -self.wB, 0]
		self.BB2 = [np.sqrt(3)/2*self.wB, 1/2.0*self.wB, 0]
		self.BB3 = [-np.sqrt(3)/2*self.wB, 1/2.0*self.wB, 0]

		#Fixed platform vertices:
		self.Bb1 = [sB/2, -self.wB, 0]
		self.Bb2 = [0, self.uB, 0]
		self.Bb3 = [-sB/2, -self.wB, 0]


		self.wP = np.sqrt(3)/6*sP
		self.uP = np.sqrt(3)/3*sP


		self.a = self.wB-self.uP
		self.b = sP/2.0 - np.sqrt(3)/2.0*self.wB
		self.c = self.wP - 0.5*self.wB

		eq = np.pi/3.0
		self.ra1 = [-sB*np.cos(eq), sB*np.sin(eq) , 0]
		self.ra2 = [-sB*np.cos(eq), -sB*np.sin(eq), 0]
		self.ra3 = [-sB, 0, 0]


		#Moving platform connection points (note: assumes known z)
		# self.PP1 = [0, -self.uP, z]
		# self.PP2 = [sP/2, self.wP, z]
		# self.PP3 = [-sP/2, wP, z]

		#Moving platform vertices (note: assumes known z)
		# self.Pp1 = [-self.uP, 0, z]
		# self.Pp2 = [self.uP*np.cos(np.pi/6), self.uP*np.sin(np.pi/6), z]
		# self.Pp3 = [self.uP*np.cos(2.*np.pi/3), self.uP*np.sin(2.*np.pi/3), z]


	def getThetas(self, position):
		#inverse kinematics
		x = position[0]
		y = position[1]
		z = position[2]

		a = self.a
		b = self.b
		c = self.c


		L = self.L
		l = self.l


		E1 = 2*L*(y+a)
		F1 = 2*z*L
		G1 = x**2 + y**2 + z**2 + a**2 + L**2 + 2*y*a - l**2

		E2 = -L*(np.sqrt(3)*(x+b)+y+c)
		F2 = 2*z*L
		G2 = x**2 + y**2 + z**2 + b**2 + c**2 + L**2 + 2*(x*b + y*c) - l**2

		E3 = L*(np.sqrt(3)*(x-b)-y-c)
		F3 = 2*z*L
		G3 = x**2 + y**2 + z**2 + b**2 + c**2 + L**2 + 2*(-x*b + y*c) - l**2

		try:
			t1 = [(-F1+np.sqrt(E1**2 + F1**2 - G1**2))/(G1-E1), (-F1-np.sqrt(E1**2 + F1**2 - G1**2))/(G1-E1)]
			t2 = [(-F2+np.sqrt(E2**2 + F2**2 - G2**2))/(G2-E2), (-F2-np.sqrt(E2**2 + F2**2 - G2**2))/(G2-E2)]
			t3 = [(-F3+np.sqrt(E3**2 + F3**2 - G3**2))/(G3-E3), (-F3-np.sqrt(E3**2 + F3**2 - G3**2))/(G3-E3)]
		except:
			return []


		try:
			theta1 = [2*np.arctan(t1[0]), 2*np.arctan(t1[1])][np.argmin(np.abs([2*np.arctan(t1[0]), 2*np.arctan(t1[1])]))]
			theta2 = [2*np.arctan(t2[0]), 2*np.arctan(t2[1])][np.argmin(np.abs([2*np.arctan(t2[0]), 2*np.arctan(t2[1])]))]
			theta3 = [2*np.arctan(t3[0]), 2*np.arctan(t3[1])][np.argmin(np.abs([2*np.arctan(t3[0]), 2*np.arctan(t3[1])]))]
		except:
			return []
		

		thetas = [theta1,theta2,theta3]
		# return thetas

		if any(np.isnan(thetas)):
			return []
		else:
			return thetas



theDR = createDR(0.524, 1.244, 0.567, 0.08)

xs = np.arange(-2,2,0.05)
ys = np.arange(-2,2,0.05)
zs = np.arange(-1.5, 0, 0.05)


fov = []
for x in xs:
	print x
	for y in ys:
		for z in zs:
			if (theDR.getThetas([x,y,z])):
				fov.append([x,y,z])
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter([k[0] for k in fov], [k[1] for k in fov], [k[2] for k in fov])
plt.ion()
plt.show()


pdb.set_trace()



####################################################################
####################################################################
####################################################################

#definitions
#
#Sb: base equilateral triangle side length
#Sp: platform equilateral triangle side length

#L: upper leg length. Legs are connected to rotational joints at points B1, B2, B3
#l: lower leg length. Legs are connected to universal joints at points A1, A2, A3

#B1, B2, B3: rotational joints at midpoints or segments on Base platform


#            *                    ^Y   
#          /   \                  |  
#         2  +  1                 |  
#        /       \                |_______>x   
#       /____3____\                      



#sB: base equilater triangle length
#sp: platform equilateral triangle length
#L: upper leg length
#l: lower leg length
#h: lower leg parallelogram width
#wB: planar distance from [0,0,0] to near base side
#uB: planar distance from [0,0,0] to base vertex
#wP: planar distance from P to near platform side
#uP: planar distance from P to a platform vertex



####################################################################################
####################################################################################


# #solve for theta1, theta2, theta3 given, x,y,z
# x = 0.2
# y = 0.2
# z = -0.5


# #femur
# L = 0.5
# #tibula
# l = 0.5


# #all units in meters, and all angles in radians (unitless)
# sB = 0.5

# wB = np.sqrt(3)/6*sB
# uB = np.sqrt(3)/3*sB

# #Fixed platform connection points
# BB1 = [0, -wB, 0]
# BB2 = [np.sqrt(3)/2*wB, 1/2.0*wB, 0]
# BB3 = [-np.sqrt(3)/2*wB, 1/2.0*wB, 0]

# #Fixed platform vertices:
# Bb1 = [sB/2, -wB, 0]
# Bb2 = [0, uB, 0]
# Bb3 = [-sB/2, -wB, 0]








# sP = 0.15

# wP = np.sqrt(3)/6*sP
# uP = np.sqrt(3)/3*sP

# a = wB-uP
# b = sP/2.0 - np.sqrt(3)/2.0*wB
# c = wP - 0.5*wB




# eq = np.pi/3.0
# ra1 = [-sB*np.cos(eq), sB*np.sin(eq) , 0]
# ra2 = [-sB*np.cos(eq), -sB*np.sin(eq), 0]
# ra3 = [-sB, 0, 0]





# #Moving platform connection points (note: assumes known z)
# PP1 = [0, -uP, z]
# PP2 = [sP/2, wP, z]
# PP3 = [-sP/2, wP, z]

# #Moving platform vertices (note: assumes known z)
# Pp1 = [-uP, 0, z]
# Pp2 = [uP*np.cos(np.pi/6), uP*np.sin(np.pi/6), z]
# Pp3 = [uP*np.cos(2.*np.pi/3), uP*np.sin(2.*np.pi/3), z]



# #inverse kinematics
# F1 = 2*z*L
# E1 = 2*L*(y+a)
# G1 = x**2 + y**2 + z**2 + a**2 + L**2 + 2*y*a - l**2

# E2 = -L*(np.sqrt(3)*(x+b)+y+c)
# F2 = 2*z*L
# G2 = x**2 + y**2 + z**2 + b**2 + c**2 + L**2 + 2*(x*b +y*c) - l**2

# E3 = L*(np.sqrt(3)*(x-b)-y-c)
# F3 = 2*z*L
# G3 = x**2 + y**2 + z**2 + b**2 + c**2 + L**2 + 2*(-x*b + y*c) - l**2


# t1 = [(-F1+np.sqrt(E1**2 + F1**2 - G1**2))/(G1-E1), (-F1-np.sqrt(E1**2 + F1**2 - G1**2))/(G1-E1)]
# t2 = [(-F2+np.sqrt(E2**2 + F2**2 - G2**2))/(G2-E2), (-F2-np.sqrt(E2**2 + F2**2 - G2**2))/(G2-E2)]
# t3 = [(-F3+np.sqrt(E3**2 + F3**2 - G3**2))/(G3-E3), (-F3-np.sqrt(E3**2 + F3**2 - G3**2))/(G3-E3)]



# theta1 = [2*np.arctan(t1[0]), 2*np.arctan(t1[1])][np.argmin(np.abs([2*np.arctan(t1[0]), 2*np.arctan(t1[1])]))]
# theta2 = [2*np.arctan(t2[0]), 2*np.arctan(t2[1])][np.argmin(np.abs([2*np.arctan(t2[0]), 2*np.arctan(t2[1])]))]
# theta3 = [2*np.arctan(t3[0]), 2*np.arctan(t3[1])][np.argmin(np.abs([2*np.arctan(t3[0]), 2*np.arctan(t3[1])]))]
# thetas = [theta1,theta2,theta3]

# # theta1d = [k*180.0/np.pi for k in theta1]
# # theta2d = [k*180.0/np.pi for k in theta2]
# # theta3d = [k*180.0/np.pi for k in theta3]


# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# #base triangle 
# xbase = [-L/2, L/2, 0, -L/2]
# ybase = [-wB, -wB, uB, -wB]
# zbase = [0, 0, 0, 0]

# #movable platform triangle
# xplat = [0, -uP, z]
# yplat = []


# #Top Leg (starts from midpoints between vertices of base traingle)
# xTopLeg = [0, wB*np.cos(np.pi/6), wB*np.cos(5.0*np.pi/6)]
# yTopLeg = [-wB, wB*np.sin(np.pi/6), wB*np.sin(5.0*np.pi/6)]
# zTopLeg = [0, 0, 0]


# #Forward kinematics:
# #Knee position
# A1 = [0, -wB-L*np.cos(theta1)]
# A2 = [np.sqrt(3.)/2.*(wB + L*np.cos(theta2)), 0.5*(wB + L*np.cos(theta2)), -L*np.sin(theta2)]
# A3 = [-np.sqrt(3.)/2. * (wB + L*np.cos(theta3)), 0.5*(wB + L*np.cos(theta3)), -L*np.sin(theta3)]


# #Top Leg Endpoint in theta=0 position
# # leg1 = [xTopLeg[0], yTopLeg[0] - L, zTopLeg[0]]
# # leg2 = [xTopLeg[1] + L*np.cos(np.pi/3), yTopLeg[1] + L*np.sin(np.pi/3), zTopLeg[1]]
# # leg3 = [xTopLeg[2] + L*np.cos(2.0*np.pi/3), yTopLeg[2] + L*np.sin(2.0*np.pi/3), zTopLeg[2]]
# # legs = [leg1, leg2, leg3]


# #unit vectors of rotational axes of driven joints
# # axBase1 = [xbase[1]-xbase[0], ybase[1]-ybase[0], 0] / np.linalg.norm([xbase[1]-xbase[0], ybase[1]-ybase[0], 0])
# # axBase2 = [xbase[2]-xbase[1], ybase[2]-ybase[1], 0] / np.linalg.norm([xbase[2]-xbase[1], ybase[2]-ybase[1], 0])
# # axBase3 = [xbase[3]-xbase[2], ybase[3]-ybase[2], 0] / np.linalg.norm([xbase[3]-xbase[2], ybase[3]-ybase[2], 0])

# # axBases = [axBase1, axBase2, axBase3]

# #driven legs onces rotated
# # nleg1 = rotateAboutAxis(axBase1, leg1, theta1)
# # nleg2 = rotateAboutAxis(axBase2, leg2, theta2)
# # nleg3 = rotateAboutAxis(axBase3, leg3, theta3)

# # rotatedLegs = [rotateAboutAxis(k[0], k[1], k[2]) for k in zip(axBases, Legs, thetas)]



# ax.plot(xbase,ybase,zbase)
# # ax.plot(xplat,yplat,zplat)
# ax.scatter(*Bb1, color = 'r', s=60)
# ax.scatter(*Bb2, color = 'r', s=60)
# ax.scatter(*Bb3, color = 'r', s=60)
# ax.scatter(*BB1, color = 'k', s=60)
# ax.scatter(*BB2, color = 'k', s=60)
# ax.scatter(*BB3, color = 'k', s=60)
# # ax.plot([xTopLeg[0], nleg1[0]], [yTopLeg[0], nleg1[1]], [zTopLeg[0], nleg1[2]])
# # ax.plot([xTopLeg[1], nleg2[0]], [yTopLeg[1], nleg2[1]], [zTopLeg[1], nleg2[2]])
# # ax.plot([xTopLeg[2], nleg3[0]], [yTopLeg[2], nleg3[1]], [zTopLeg[2], nleg3[2]])
# plt.ion()
# plt.show()

# ####################################################################
# ####################################################################
# ####################################################################




#platform triangle
xplat = []

pdb.set_trace()







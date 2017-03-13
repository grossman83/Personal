#delta robot kinematics

import numpy as np
import marcmath

import pdb



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



#ra1, ra2, ra3: rotational axes about which the upper legs are rotated.


#solve for theta1, theta2, theta3 given, x,y,z
x = 0.2
y = 0.2
z = -0.7


#femur
L = 0.5
#tibula
l = 0.5


#all units in meters, and all angles in radians (unitless)
sB = 0.5

wB = np.sqrt(3)/6*sB
uB = np.sqrt(3)/3*sB

B1 = [0, -wB, 0]
B2 = [np.sqrt(3)/2*wB, 1/2.0*wB, 0]
B3 = [-np.sqrt(3)/2*wB, 1/2.0*wB, 0]


sP = 0.15

wP = np.sqrt(3)/6*sP
uP = np.sqrt(3)/3*sP

a = wB-uP
b = sP/2.0 - np.sqrt(3)/2.0*wB
c = wP - 0.5*wB




eq = np.pi/3.0

B1 = [sB-sB*np.cos(eq)/sB, 0]
B2 = [-sB*np.cos(eq)/2, 0]
B3 = [0, -sB*np.sin(eq)/2]


ra1 = [-sB*np.cos(eq), sB*np.sin(eq) , 0]
ra2 = [-sB*np.cos(eq), -sB*np.sin(eq), 0]
ra3 = [-sB, 0, 0]


#inverse kinematics
F1 = 2*z*L
E1 = 2*L*(y+a)
G1 = x**2 + y**2 + z**2 + a**2 + L**2 + 2*y*a - l**2

E2 = -L*(np.sqrt(3)*(x+b)+y+c)
F2 = 2*z*L
G2 = x**2 + y**2 + z**2 + b**2 + c**2 + L**2 + 2*(x*b +y*c) - l**2

E3 = L*(np.sqrt(3)*(x-b)-y-c)
F3 = 2*z*L
G3 = x**2 + y**2 + z**2 + b**2 + c**2 + L**2 + 2*(-x*b + y*c) - l**2


t1 = [(-F1+np.sqrt(E1**2 + F1**2 - G1**2))/(G1-E1), (-F1-np.sqrt(E1**2 + F1**2 - G1**2))/(G1-E1)]
t2 = [(-F2+np.sqrt(E2**2 + F2**2 - G2**2))/(G2-E2), (-F2-np.sqrt(E2**2 + F2**2 - G2**2))/(G2-E2)]
t3 = [(-F3+np.sqrt(E3**2 + F3**2 - G3**2))/(G3-E3), (-F3-np.sqrt(E3**2 + F3**2 - G3**2))/(G3-E3)]



theta1 = [2*np.arctan(t1[0]), 2*np.arctan(t1[1])]
theta2 = [2*np.arctan(t2[0]), 2*np.arctan(t2[1])]
theta3 = [2*np.arctan(t3[0]), 2*np.arctan(t3[1])]

pdb.set_trace()







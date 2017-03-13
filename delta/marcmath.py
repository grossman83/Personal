# additional math stuff


import numpy as np


def sind(theta):
	return np.sin(theta*np.pi/180.)

def cosd(theta):
	return np.cos(theta*np.pi/180.)

def tand(theta):
	return np.tan(theta*np.pi/180.)


def asind(ratio):
	return np.arcsin(ratio)*180.0/np.pi

def acosd(ratio):
	return np.arccos(ratio)*180.0/np.pi

def atand(ratio):
	return np.arctan(ratio)*180.0/np.pi


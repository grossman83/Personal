import numpy as np
import sys
sys.path.append('../scripts')
import matplotlib.pyplot as plt
plt.ion()

from shapely.geometry import LineString, Point, LinearRing, Polygon, MultiPolygon

from shapelyTools import shapelyDisp, shapelyRemove

from shapely.ops import cascaded_union
from shapely.affinity import translate, rotate

import pdb


threadPitch = 0.0625
threadPitchE = threadPitch * 0.9999999
threadDepth = 0.04


boltOD = 0.742
boltLength = 1
# externalThreadDepth = threadPitchE*np.sqrt(3)/2
externalThreadDepth = threadDepth


nutID = 0.7
nutOD = 1.0
nutLength = 0.5
# internalThreadDepth = threadPitchE*np.sqrt(3)/2
internalThreadDepth = threadDepth



class cutter:
	def __init__(includedAngle, length, tipRadius):
		self.includedAngle = includedAngle
		self.length = length
		self.tipRadius = tipRadius

		#now create the cutter geometry with tip down and tip tangent to (0,0)
		#	\       /
		#	 \     /
		#	  \   /
		#	   \ /
		#	    U
		tipCircle

class bolt:
	def __init__(self, boltOD, boltLength, threadPitch, threadDepth):
		self.boltOD = boltOD
		self.boltLen = boltLength
		self.pitch = threadPitch
		self.threadDepth = threadDepth
		self.polygon = Polygon([(0, self.boltOD/2), (self.boltLen, self.boltOD/2), (self.boltLen, -1*self.boltOD/2), (0, -1*self.boltOD/2)])

class nut:
	def __init__(self, nutID, nutOD, nutLength, threadPitch, threadDepth):
		self.ID = nutID
		self.OD = nutOD
		self.length = nutLength
		self.pitch = threadPitch
		self.threadDepth = threadDepth
		topPolygon = Polygon([(0, self.ID/2.0), (self.length, self.ID/2.0), (self.length, self.OD/2.0), (0, self.OD/2)])
		botPolygon = Polygon([(0, -self.ID/2.0), (self.length, -self.ID/2.0), (self.length, -self.OD/2.0), (0, -self.OD/2)])
		self.polygon = MultiPolygon([topPolygon, botPolygon])


def cutExternalThreads(bolt):
	#takes the bolt object and cuts threads into it
	numThreads = int(bolt.boltLen / bolt.pitch)+1

	#create the triangle that will cut the bolt. It's overly large on purpose
	cutLeg = 0.5*bolt.boltOD
	triangle = Polygon([(0,0), (-0.5*cutLeg, 0.5*np.sqrt(3)*cutLeg), (0.5*cutLeg, 0.5*np.sqrt(3)*cutLeg)])
	newTriangle = translate(triangle, yoff = bolt.boltOD/2 - bolt.threadDepth)
	
	topTriangles = [newTriangle]
	for k in range(numThreads):
		topTriangles.append(translate(newTriangle, xoff=k*bolt.pitch))
	topCut = cascaded_union(topTriangles)
	
		

	#rotate original triangle and translate to cut bottom threads
	newTriangle = rotate(triangle, 180, origin=(0,0), use_radians=False)
	newTriangle = translate(newTriangle, xoff = bolt.pitch/2, yoff = -bolt.boltOD/2 + bolt.threadDepth)

	botTriangles = [newTriangle]
	for k in range(numThreads):
		botTriangles.append(translate(newTriangle, xoff = k*bolt.pitch))
	botCut = cascaded_union(botTriangles)

	bolt.polygon = bolt.polygon.difference(topCut)
	bolt.polygon = bolt.polygon.difference(botCut)

	return bolt

def cutInternalThreads(nut):
	#takes the initial nut object and cuts the interal threads into its geometry
	numThreads = int(nut.length / nut.pitch) + 2

	#create the trinagles that will cut the nut. They're oversize on purpose.
	cutLeg = 0.5*nut.ID
	triangle = Polygon([(0,0), (-0.5*cutLeg, 0.5*np.sqrt(3)*cutLeg), (0.5*cutLeg, 0.5*np.sqrt(3)*cutLeg)])
	newTriangle = translate(triangle, yoff = -nut.ID/2 - nut.threadDepth)

	botTriangles = [newTriangle]
	for k in range(numThreads):
		botTriangles.append(translate(newTriangle, xoff=k*nut.pitch))
	botCut = cascaded_union(botTriangles)

	#rotate triangle and translate upwards to make top cut
	newTriangle = rotate(triangle, 180, origin = (0,0), use_radians=False)
	newTriangle = translate(newTriangle, xoff = nut.pitch/2.0, yoff = nut.ID/2.0+nut.threadDepth)

	topTriangles = [newTriangle]
	for k in range(numThreads):
		topTriangles.append(translate(newTriangle, xoff = k*nut.pitch))
	topCut = cascaded_union(topTriangles)

	nut.polygon = nut.polygon.difference(topCut)
	nut.polygon = nut.polygon.difference(botCut)

	return nut

def createBoltOutline(boltOD):
	#threaded bolt face starts at [0,0], and head is at [boltLength, boldOD/2]\
	boltOutline = Polygon([[0,boltOD/2], [boltLength, boltOD/2], [boltLength, -1* boltOD/2], [0, -1*boltOD/2]])
	return boltOutline

def createBoltThreads(boltOD, threadPitch, externalThreaddDepth):
	#start top thread at (0,boltOD/2), and bottom thread at (threadPitch/2, -boltOD/2)
	numTriangles = boltLength/threadPitch
	topTriangleCoordsX = [k*threadPitch for k in range(int(numTriangles)+1)]
	topTriangleCoordsY = [boltOD/2-externalThreadDepth for k in topTriangleCoordsX]

	botTriangleCoordsX = [k*threadPitch+threadPitch/2 for k in range(int(numTriangles))]
	botTriangleCoordsY = [-boltOD/2+externalThreadDepth for k in topTriangleCoordsX]

	topTrianglePts = [Point(k[0],k[1]) for k in zip(topTriangleCoordsX,topTriangleCoordsY)]
	botTrianglePts = [Point(k[0],k[1]) for k in zip(botTriangleCoordsX,botTriangleCoordsY)]

	triangles = []
	for k in topTrianglePts:
		#start with bottom point
		triangles.append(Polygon([(k.x,k.y), (k.x + threadPitchE*0.5, k.y + np.sqrt(3)/2*threadPitchE), (k.x-threadPitch*0.5, k.y + np.sqrt(3)/2*threadPitchE)]))
	
	for k in botTrianglePts:
		triangles.append(Polygon([(k.x,k.y), (k.x + threadPitchE*0.5, k.y - np.sqrt(3)/2*threadPitchE), (k.x-threadPitch*0.5, k.y - np.sqrt(3)/2*threadPitchE)]))

	topThreads = MultiPolygon(triangles)

	return topThreads

def createNutOutline(nutID, nutOD, nutLength):
	topNutOutline = Polygon([(0, nutID/2), (0, nutOD/2), (nutLength, nutOD/2), (nutLength, nutID/2)])
	botNutOutline = Polygon([(0, -nutID/2), (0, -nutOD/2), (nutLength, -nutOD/2), (nutLength, -nutID/2)])
	return MultiPolygon([topNutOutline, botNutOutline])

def createNutThreads(nutID, nutLength, threadPitch):
	numTriangles = nutLength/threadPitch
	topTriangleCoordsX = [k*threadPitch - 0.5*threadPitch for k in range(int(numTriangles)+1)]
	topTriangleCoordsY = [nutID/2+internalThreadDepth for k in topTriangleCoordsX]

	botTriangleCoordsX = [k*threadPitch for k in range(int(numTriangles)+1)]
	botTriangleCoordsY = [-nutID/2-internalThreadDepth for k in topTriangleCoordsX]

	topTrianglePts = [Point(k[0],k[1]) for k in zip(topTriangleCoordsX, topTriangleCoordsY)]
	botTrianglePts = [Point(k[0],k[1]) for k in zip(botTriangleCoordsX, botTriangleCoordsY)]

	triangles = []
	for k in topTrianglePts:
		triangles.append(Polygon([(k.x,k.y), (k.x + threadPitchE*0.5, k.y - np.sqrt(3)/2*threadPitchE), (k.x - threadPitch*0.5, k.y-np.sqrt(3)/2*threadPitchE)]))

	for k in botTrianglePts:
		triangles.append(Polygon([(k.x,k.y), (k.x + threadPitchE*0.5, k.y + np.sqrt(3)/2*threadPitchE), (k.x - threadPitch*0.5, k.y+np.sqrt(3)/2*threadPitchE)]))

	topThreads = MultiPolygon(triangles)

	return topThreads




bolt1 = bolt(boltOD, boltLength, threadPitch, externalThreadDepth)
nut1 = nut(nutID, nutOD, nutLength, threadPitch, internalThreadDepth)

blah = cutExternalThreads(bolt1)

muah = cutInternalThreads(nut1)

shapelyDisp([bolt1.polygon, nut1.polygon])

pdb.set_trace()







pdb.set_trace()




# boltOutline = createBoltOutline(boltOD)
# topThreads = createBoltThreads(boltOD, threadPitch, externalThreadDepth)
# threadedBoltOutline = boltOutline.difference(topThreads)
# shapelyDisp(threadedBoltOutline, color = 'b')
# # pdb.set_trace()




# nutOutline = createNutOutline(nutID, nutOD, nutLength)
# nutThreads = createNutThreads(nutID, nutLength, threadPitch)
# threadedNutOutline = nutOutline.difference(nutThreads)
# shapelyDisp(threadedNutOutline, color = 'r')


# shapelyDisp(boltOutline)
# shapelyDisp(topThreads)
# plt.show(block=True)

# newBolt = boltOutline(topThreads)
# shapelyDisp(newBolt)

plt.ion()
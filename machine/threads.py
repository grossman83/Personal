import numpy as np
import sys
sys.path.append('../scripts')
import matplotlib.pyplot as plt
plt.ion()

from shapely.geometry import LineString, Point, LinearRing, Polygon, MultiPolygon

from shapelyTools import shapelyDisp, shapelyRemove

import pdb


boltOD = 0.75
boltLength = 4
threadPitch = 0.125
threadPitchE = 0.9999999*threadPitch
threadDepth = 0.035


def createBoltOutline(boltOD, threadDepth):
	#threaded bolt face starts at [0,0], and head is at [boltLength, boldOD/2]\
	boltOutline = Polygon([[0,boltOD/2], [boltLength, boltOD/2], [boltLength, -1* boltOD/2], [0, -1*boltOD/2]])
	return boltOutline

def createBoltThreads(boltOD, threadPitch, threadDepth):
	#start top thread at (0,boltOD/2), and bottom thread at (threadPitch/2, -boltOD/2)
	numTriangles = boltLength/threadPitch
	topTriangleCoordsX = [k*threadPitch for k in range(int(numTriangles)+1)]
	topTriangleCoordsY = [boltOD/2-threadDepth for k in topTriangleCoordsX]

	botTriangleCoordsX = [k*threadPitch+threadPitch/2 for k in range(int(numTriangles))]
	botTriangleCoordsY = [-boltOD/2+threadDepth for k in topTriangleCoordsX]

	topTrianglePts = [Point(k[0],k[1]) for k in zip(topTriangleCoordsX,topTriangleCoordsY)]
	botTrianglePts = [Point(k[0],k[1]) for k in zip(botTriangleCoordsX,botTriangleCoordsY)]

	triangles = []
	for k in topTrianglePts:
		#start with bottom point
		triangles.append(Polygon([(k.x,k.y), (k.x + threadPitch*0.5, k.y + np.sqrt(3)/2*threadPitch), (k.x-threadPitch*0.5, k.y + np.sqrt(3)/2*threadPitch)]))
	
	for k in botTrianglePts:
		triangles.append(Polygon([(k.x,k.y), (k.x + threadPitch*0.5, k.y - np.sqrt(3)/2*threadPitch), (k.x-threadPitch*0.5, k.y - np.sqrt(3)/2*threadPitch)]))

	topThreads = MultiPolygon(triangles)

	return topThreads




boltOutline = createBoltOutline(boltOD, threadDepth)
topThreads = createBoltThreads(boltOD, threadPitch, threadDepth)

threadedBoltOutline = boltOutline.difference(topThreads)
shapelyDisp(threadedBoltOutline)
pdb.set_trace()

# shapelyDisp(boltOutline)
# shapelyDisp(topThreads)
# plt.show(block=True)

newBolt = boltOutline(topThreads)
shapelyDisp(newBolt)

plt.ion()

pdb.set_trace()

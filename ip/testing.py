import sys, os
import numpy as np
import cv2
import pdb
import matplotlib.pyplot as plt


if __name__ =='__main__':
	
	

	#create an array of 50x50x3 between 0 and 255
	blah = np.random.randint(0,255, (100,100,3), dtype=np.uint8)

	#now bit-shift


	pdb.set_trace()

	window_name = 'image'
	cv2.imshow(window_name, blah)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	pdb.set_trace()

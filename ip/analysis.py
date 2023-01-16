import sys, os
import numpy as np
import cv2
import pdb
import matplotlib.pyplot as plt


if __name__ =='__main__':
	
	infile_path = sys.argv[1]

	root_path = os.path.expanduser('~')
	infile_path = os.path.join(root_path, infile_path)

	outfile_path = os.path.join(root_path, infile_path)[0:-4]+'4'+'.png'


	# read the image
	im = cv2.imread(infile_path)

	# lots of numpy stuff applies to the image now as it's simply an n-d array
	# of shape 540x1438x3. Not yet sure if it's BGR or RGB.

	#now I've flattened them
	im_b = im[:,:,0]
	im_g = im[:,:,1]
	im_r = im[:,:,2]


	#bit shift every pixel two bits to the right. (divide by 4)
	if True:
		im6bit = np.right_shift(im, 2)
		im6bitback = np.left_shift(im6bit, 2)
		outfile_path = os.path.join(root_path, infile_path)[0:-4]+'6bit_full_range'+'.png'
		cv2.imwrite(outfile_path, im6bitback)



	#take a sample in the middle of the range. This didn't prove very useful
	if False:
		blah = np.random.randint(0, 255,[10,10,3], np.uint8)
		blah255 = 255 * np.ones([10,10], dtype=np.uint8)
		blah0 = np.zeros([10,10], dtype=np.uint8)

		blah255_b = np.where(blah[:,:,0]>160, blah255, blah[:,:,0])
		blah255_g = np.where(blah[:,:,1]>160, blah255, blah[:,:,1])
		blah255_r = np.where(blah[:,:,2]>160, blah255, blah[:,:,2])



	outfile_path = os.path.join(root_path, infile_path)[0:-4]+'_8-bit'+'.png'
	cv2.imwrite(outfile_path, im)


	im255 = np.ones(np.array(np.shape(im)[0:2]), dtype=np.uint8) * 255
	im0 = np.zeros(np.array(np.shape(im)[0:2]), dtype=np.uint8)

	im7bit_b = np.where(im[:,:,0]>127, im255, im[:,:,0])
	im7bit_g = np.where(im[:,:,1]>127, im255, im[:,:,1])
	im7bit_r = np.where(im[:,:,2]>127, im255, im[:,:,2])

	im7bit_b = np.left_shift(im7bit_b, 1)
	im7bit_g = np.left_shift(im7bit_g, 1)
	im7bit_r = np.left_shift(im7bit_r, 1)

	im7bit = np.stack((im7bit_b, im7bit_g, im7bit_r), axis=2)
	outfile_path = os.path.join(root_path, infile_path)[0:-4]+'_7-bit'+'.png'
	cv2.imwrite(outfile_path, im7bit)


	im6bit_b = np.where(im[:,:,0]>63, im255, im[:,:,0])
	im6bit_g = np.where(im[:,:,1]>63, im255, im[:,:,1])
	im6bit_r = np.where(im[:,:,2]>63, im255, im[:,:,2])

	im6bit_b = np.left_shift(im6bit_b, 2)
	im6bit_g = np.left_shift(im6bit_g, 2)
	im6bit_r = np.left_shift(im6bit_r, 2)

	im6bit = np.stack((im6bit_b, im6bit_g, im6bit_r), axis=2)
	outfile_path = os.path.join(root_path, infile_path)[0:-4]+'_6-bit'+'.png'
	cv2.imwrite(outfile_path, im6bit)


	# pdb.set_trace()
	#cedric and I chatted and it doesn't seem to make sense to put everyting
	#below some value as a zero.
	# im0_b = np.where(im255[:,:,0]<90, im0, im255[:,:,0])
	# im0_g = np.where(im255[:,:,1]<90, im0, im255[:,:,1])
	# im0_r = np.where(im255[:,:,2]<90, im0, im255[:,:,2])

	# im6bitmiddle = np.stack((im0_b, im0_g, im0_r), axis=2)

	# outfile_path = os.path.join(root_path, infile_path)[0:-4]+'7-bit'+'.png'
	# cv2.imwrite(outfile_path, im128)

	pdb.set_trace()



	ceil = 160 * np.ones(np.array(np.shape(im)))

	


	#make an array of blue only pixels
	blue = np.zeros(np.array(np.shape(im)), dtype=np.uint8)
	blue[:,:,0] = 255

	blah = np.where(im<254, im[:,:,], blue)


	# pdb.set_trace()

	# window_name = 'image'
	# cv2.imshow(window_name, im6bitback)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()



	#now to create a histogram of the pixel values in each of the color channels
	nbins = 255
	fig, axs = plt.subplots(1,3, sharey=True, tight_layout=True)
	axs[0].hist(im_b.flatten(), bins=nbins)
	axs[1].hist(im_g.flatten(), bins=nbins)
	axs[2].hist(im_r.flatten(), bins=nbins)

	nbins = 255
	fig2, axs2 = plt.subplots(1,3, sharey=True, tight_layout=True)
	axs2[0].hist(im6bitback[:,:,0].flatten(), bins=nbins)
	axs2[1].hist(im6bitback[:,:,1].flatten(), bins=nbins)
	axs2[2].hist(im6bitback[:,:,2].flatten(), bins=nbins)

	plt.ion()
	plt.show()


	# I'd like to find any pixel that is saturated and make it blue. This would
	# stand out in the image and we coudld think about what to do about it.
	#Searching to find all saturaged pixels.
	# np.where



	#show the image
	# window_name = 'image'
	# cv2.imshow(window_name, im)
	# cv2.waitKey(0)
	# closing all open windows
	# cv2.destroyAllWindows()
	


	# any(im_r>254)

	pdb.set_trace()

import sys, os
import numpy as np
import cv2
import pdb
import matplotlib.pyplot as plt



def get_sat_image(im, l_sat, h_sat):
	#make every pixel that is saturated in any chanel yellow and any pixel
	#that is zero in any channel blue. Return that image.
	#@TODO Still not working quite right as it only replaces the value in the
	#specific channel not the entire pixel value.
	
	#create a full blue image of same size as im
	im255 = np.ones(np.array(np.shape(im)), dtype=np.uint8) * 255
	im255[:,:,1] = 0
	im255[:,:,2] = 0
	blue = im255

	#create a full yellow image of same size as im
	im255 = np.ones(np.array(np.shape(im)), dtype=np.uint8) * 255
	im255[:,:,0] = 0
	yellow = im255


	#create boolean masks
	bmask_h = (im[:,:,0] >= h_sat) | (im[:,:,1] >= h_sat) | (im[:,:,2] >= h_sat)
	bmask_hx = np.stack([bmask_h, bmask_h, bmask_h], axis=2)
	bmask_l = (im[:,:,0] <= l_sat) | (im[:,:,1] <= l_sat) | (im[:,:,2] <= l_sat)
	bmask_lx = np.stack([bmask_l, bmask_l, bmask_l], axis=2)

	#now anywhere the high mask is true replaec the pixel with yellow
	sat_h = np.where(bmask_hx, yellow, im)
	composite_sat_image = np.where(bmask_lx, blue, sat_h)

	return composite_sat_image


def get_reduced_image(im, n_bits):
	imnbit = np.right_shift(im, n_bits)
	return np.left_shift(imnbit, n_bits)


def brighten_lows(im):
	im_b = im * np.exp(np.log10(265-im))
	im_bb = im_b / np.max(im_b) * 255
	return im_bb.astype(np.uint8)



if __name__ =='__main__':
	
	infile_path = sys.argv[1]

	root_path = os.path.expanduser('~')
	infile_path = os.path.join(root_path, infile_path)
	im = cv2.imread(infile_path)


	#save the original file
	outfile_path = os.path.join(root_path, infile_path)[0:-4]+'_8-bit'+'.png'
	cv2.imwrite(outfile_path, im)

	##Brighten the dark spots of the image
	im_l = (im[:,:,0] <= 127) & (im[:,:,1] <= 127) & (im[:,:,2] <= 127)
	bmask_l = np.stack([im_l, im_l, im_l], axis=2)
	twos = 2*np.ones(np.shape(im))
	twos = twos * bmask_l
	ones = np.ones(np.shape(im))
	mult_mask = np.where(twos == 2, twos, ones)

	bright_im = im * mult_mask
	outfile_path = os.path.join(root_path, infile_path)[0:-4]+'_8-bit-brightened'+'.png'
	cv2.imwrite(outfile_path, bright_im)


	nbins = 255
	fig, axs = plt.subplots(1,3, sharey=True, tight_layout=True)
	axs[0].hist(im[:,:,0].flatten(), bins=nbins)
	axs[1].hist(im[:,:,1].flatten(), bins=nbins)
	axs[2].hist(im[:,:,2].flatten(), bins=nbins)
	fig.savefig(outfile_path[0:-4]+'-hist.png')

	
	#brighten the lows on a log scale
	im_b = brighten_lows(im)
	pdb.set_trace()



	#OUTPUT THE SATURATED IMAGE
	sat_im = get_sat_image(im, 0, 255)
	outfile_path = os.path.join(root_path, infile_path)[0:-4]+'_8-bit-sat'+'.png'
	cv2.imwrite(outfile_path, sat_im)



	########################### 6 bit full range ############################
	# bit shift every pixel two bits to the right. (divide by 4)
	# Then shift it back to the left (multiply by 4)
	# interestingly enough a 6 bit image that spans the entire range of an 8 bit
	# image is nearly indistinguishable.
	# im6bit = np.right_shift(im, 2)
	# im6bitback = np.left_shift(im6bit, 2)

	im6bit = get_reduced_image(im, 2)
	outfile_path = os.path.join(root_path, infile_path)[0:-4]+'_6bit_full_range'+'.png'
	cv2.imwrite(outfile_path, im6bit)

	sat_im = get_sat_image(im6bit, 0, 252)
	outfile_path = os.path.join(root_path, infile_path)[0:-4]+'_6bit_full_range-sat'+'.png'
	cv2.imwrite(outfile_path, sat_im)

	nbins = 255
	fig, axs = plt.subplots(1,3, sharey=True, tight_layout=True)
	axs[0].hist(im6bit[:,:,0].flatten(), bins=nbins)
	axs[1].hist(im6bit[:,:,1].flatten(), bins=nbins)
	axs[2].hist(im6bit[:,:,2].flatten(), bins=nbins)
	fig.savefig(outfile_path[0:-4]+'_6-bit-full_range-hist.png')	
	########################### 6 bit full range ############################
	




	#######################  7 BIT WORK   ##################################
	im7bit = np.clip(im, 2, 255)
	outfile_path = os.path.join(root_path, infile_path)[0:-4]+'_7-bit2-255'+'.png'
	cv2.imwrite(outfile_path, im7bit)


	sat_im = get_sat_image(im7bit, 2, 255)
	outfile_path = os.path.join(root_path, infile_path)[0:-4]+'_7bit-sat2-255'+'.png'
	cv2.imwrite(outfile_path, sat_im)



	nbins = 255
	fig, axs = plt.subplots(1,3, sharey=True, tight_layout=True)
	axs[0].hist(im7bit[:,:,0].flatten(), bins=nbins)
	axs[1].hist(im7bit[:,:,1].flatten(), bins=nbins)
	axs[2].hist(im7bit[:,:,2].flatten(), bins=nbins)
	fig.savefig(outfile_path[0:-4]+'-hist.png')
	#######################  7 BIT WORK   ##################################



	#######################  6 BIT WORK   ##################################
	im6bit = np.clip(im, 4, 255)
	# im6bit = np.right_shift(im6bit, 2)
	outfile_path = os.path.join(root_path, infile_path)[0:-4]+'_6-bit'+'.png'
	cv2.imwrite(outfile_path, im6bit)

	sat_im = get_sat_image(im6bit, 4, 255)
	outfile_path = os.path.join(root_path, infile_path)[0:-4]+'_6-bit-sat'+'.png'
	cv2.imwrite(outfile_path, sat_im)

	nbins = 255
	fig, axs = plt.subplots(1,3, sharey=True, tight_layout=True)
	axs[0].hist(im6bit[:,:,0].flatten(), bins=nbins)
	axs[1].hist(im6bit[:,:,1].flatten(), bins=nbins)
	axs[2].hist(im6bit[:,:,2].flatten(), bins=nbins)
	fig.savefig(outfile_path[0:-4]+'-hist.png')
	#######################  6 BIT WORK   ##################################


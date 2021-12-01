from PyPDF2 import PdfFileReader, PdfFileWriter, pdf
import math
import os
import pdb
import sys

# USAGE
# This utility is designed to stitch together landscape pdfs of the 11x17 size
# as "printed to pdf" from the OneNote web-app. This has only been tested on
# a Macbook Pro running OS 10.14.3 and using the latest Chrome browser as of
# 20DEC2020

# To run this utility you will need the PyPDF2 package. It was a simple pip
# installation for me. I do not believe there are any other python dependencies.

# Run in command like this:
# python pdf_stitch.py "~/dir/input file.pdf" "~/dir/output_file.pdf"


# Quick notes
# This assumes that the file is in the user's space (~/).
# This can be pretty slow [> 10-20 seconds] for larger pdfs. Not sure why.

# Information on PyPDF2 here: https://pythonhosted.org/PyPDF2/index.html



if __name__ =='__main__':
	
	infile_path = sys.argv[1]
	outfile_path = sys.argv[2]

	root_path = os.path.expanduser('~')
	infile_path = os.path.join(root_path, infile_path)
	outfile_path = os.path.join(root_path, outfile_path)

	#The height had to be hard coded. No-where in the pdf file could I find
	#a value that matched the correct stitching value of 736 in the vertical.
	#Similar story for the width.

	#DPI does appear to be 72. We can get this by doing 792/11 = 72
	# we can also get there by doing 1224/17 = 72
	# that said there do appear to be some margins. This

	page_actual_height = 736
	page_actual_width = 1224


	# tabloid portrait
	page_actual_height = 1224
	page_actual_width = 792

	# letter landscape
	# page_actual_height = 556.5
	# page_actual_width = 745

	# letter portrait
	# page_actual_height = 687
	# page_actual_width = 556.5

	#Tabloid size paper 11x17 (landscape = 17x11)
	#Mediabox size 1224, 792

	#Letter Size 8.5x11 or 11x8.5 landscape
	#mediabox is 792x612
	# creating a pdf File object of original pdf 
	pdfFileObj = open(infile_path, 'rb') 

	# creating a pdf Reader object 
	pdfReader = PdfFileReader(pdfFileObj) 

	# creating a pdf writer object for new pdf 
	pdfWriter = PdfFileWriter() 
	num_pages = pdfReader.getNumPages()

	#create a list of pages
	pages = [pdfReader.getPage(k) for k in range(num_pages)]
	

	trimboxes = [k.trimBox for k in pages]
	page_width = trimboxes[0].getWidth()
	page_height = trimboxes[0].getHeight()


	#set the total height of the pdf
	page_buffer_tabloid = 52
	page_ybuffer_letter = 0
	page_xbuffer_letter = 55.5
	total_height = num_pages * page_actual_height + page_ybuffer_letter
	total_width = page_actual_width
	total_width = page_actual_width * 4

	# pdb.set_trace()
	#create an empty page the size of the total of the pages
	# blank_page = pdf.PageObject.createBlankPage(width=total_width, height=total_height)

	#need to figure out a way to count the nubmer of pages and figure out how
	#they're all supposed to fit together. Example shown below.
	# 1   2   3
	# 4   5
	# 6   7   8   9
	# 10  11
	# 12


	##@MARC todo set things up for pdfs that are of varying page widths.

	# #create a list that explains the order of the pages.
	# page_list = [[1, 2, 3],[4, 5, 6], [7, 8]]
	# # create a blank page the size of the expected set of combined pages
	# canvas_height = len(page_list) * page_actual_height
	# canvas_width = max(len(k) for k in page_list) * (page_actual_width + page_xbuffer_letter)
	# blank_page = pdf.PageObject.createBlankPage(width=canvas_width, height=canvas_height)

	# idy = len(page_list) - 1
	# for h_page_list in page_list:
	# 	for page_idx, page_id in zip(range(len(h_page_list)), h_page_list):
	# 		# pdb.set_trace()
	# 		print('idy: {0}: '.format(idy))
	# 		print('page_idx: {0}'.format(page_idx))
	# 		print('page_id: {0}'.format(page_id))
	# 		blank_page.mergeTranslatedPage(
	# 			pages[page_id-1],
	# 			page_idx * (page_actual_width + page_xbuffer_letter),
	# 			idy*page_actual_height)
	# 	idy = idy - 1

	canvas_height = len(pages) * page_actual_height
	canvas_width = 1 * page_actual_width
	blank_page = pdf.PageObject.createBlankPage(width=canvas_width, height=canvas_height)

	# pdb.set_trace()	
	pages.reverse()
	for idy, page in enumerate(pages):
		blank_page.mergeTranslatedPage(page, 0, idy * page_actual_height)




	pdfWriter.addPage(blank_page)

	newFile = open(outfile_path, 'wb') 

	# writing rotated pages to new file 
	pdfWriter.write(newFile) 

	# closing the original pdf file object 
	pdfFileObj.close() 

	# closing the new pdf file object 
	newFile.close() 
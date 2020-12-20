from PyPDF2 import PdfFileReader, PdfFileWriter, pdf
import math
import os
import pdb
import sys



if __name__ =='__main__':
	
	infile_path = sys.argv[1]
	outfile_path = sys.argv[2]

	root_path = os.path.expanduser('~')
	infile_path = os.path.join(root_path, infile_path)
	outfile_path = os.path.join(root_path, outfile_path)

	#the height had to be hard coded. No-where in the pdf file could I find
	#a value that matched the correct stitching value of 736 in the vertical.
	#Similar story for the width.
	page_actual_height = 736
	page_actual_width = 1224

	#Tabloid size paper 11x17 (landscape = 17x11)
	#Mediabox size 1224, 792
	pdb.set_trace()
	# creating a pdf File object of original pdf 
	pdfFileObj = open(infile_path, 'rb') 

	# creating a pdf Reader object 
	pdfReader = PdfFileReader(pdfFileObj) 

	# creating a pdf writer object for new pdf 
	pdfWriter = PdfFileWriter() 
	num_pages = pdfReader.getNumPages()

	#create a list of pages
	pages = [pdfReader.getPage(k) for k in range(num_pages)]
	
	#set the total height of the pdf
	total_height = num_pages * page_actual_height + 52
	total_width = page_actual_width

	# pdb.set_trace()	
	#create an empty page the size of the total of the pages
	blank_page = pdf.PageObject.createBlankPage(width=total_width, height=total_height)

	# pdb.set_trace()
	#merge pages
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
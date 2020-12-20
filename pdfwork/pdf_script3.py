from PyPDF2 import PdfFileReader, PdfFileWriter, pdf
import math
import os
import pdb
import sys



if __name__ =='__main__':
	root_path = os.path.expanduser('~')
	file_path = os.path.join(root_path, 'Desktop', 'Master Panel Subset.pdf')
	outpath = os.path.join(root_path, 'Desktop', 'Master PCBA.pdf')

	
	page_actual_height = 686
	page_actual_width = 500

	row_width = [2, 2, 2, 3, 3, 3, ]

	buffered_row_width = 

	canvas_width = max(row_width) * page_actual_width

	# creating a pdf File object of original pdf 
	pdfFileObj = open(file_path, 'rb') 

	# creating a pdf Reader object 
	pdfReader = PdfFileReader(pdfFileObj) 

	# creating a pdf writer object for new pdf 
	pdfWriter = PdfFileWriter() 
	num_pages = pdfReader.getNumPages()

	#create a list of pages
	pages = [pdfReader.getPage(k) for k in range(num_pages)]
	
	#set the total height of the pdf
	canvas_height = len(row_width) * page_actual_height + 52
	canvas_width = canvas_width

	#create an empty page the size of the total of the pages
	blank_page = pdf.PageObject.createBlankPage(
		width=canvas_width,
		height=canvas_height)

	#merge pages
	pages.reverse()
	for idy in row_width:
		for idx, page in enumerate(pages):
			blank_page.mergeTranslatedPage(page, 0, idy * page_actual_height)

	pdfWriter.addPage(blank_page)

	newFile = open(outpath, 'wb') 

	# writing rotated pages to new file 
	pdfWriter.write(newFile) 

	# closing the original pdf file object 
	pdfFileObj.close() 

	# closing the new pdf file object 
	newFile.close()










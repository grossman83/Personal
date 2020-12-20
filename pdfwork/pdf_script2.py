from PyPDF2 import PdfFileReader, PdfFileWriter, pdf
import math
import os
import pdb



if __name__ =='__main__':
	root_path = os.path.expanduser('~')
	file_path = os.path.join(root_path, 'Desktop', 'Hot Water Heater and Recirculation Pump.pdf')
	outpath = os.path.join(root_path, 'Desktop', 'Hot Water Heater.pdf')

	
	page_actual_height = 686
	pdf_actual_width = 1


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
	total_height = num_pages * page_actual_height + 52
	total_width = pages[0].artBox[2]

	#create an empty page the size of the total of the pages
	blank_page = pdf.PageObject.createBlankPage(width=total_width, height=total_height)

	pdb.set_trace()
	#merge pages
	pages.reverse()
	for idy, page in enumerate(pages):
		blank_page.mergeTranslatedPage(page, 0, idy * page_actual_height)

	pdfWriter.addPage(blank_page)

	newFile = open(outpath, 'wb') 

	# writing rotated pages to new file 
	pdfWriter.write(newFile) 

	# closing the original pdf file object 
	pdfFileObj.close() 

	# closing the new pdf file object 
	newFile.close() 
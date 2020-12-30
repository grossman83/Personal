from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import pdb



def get_info(path):
	with open (file_path, 'rb') as pdfFileObj:
		pdfReader = PdfFileReader(pdfFileObj)
		info = pdf.getDocumentInfo()
		number_of_pages = pdf.getNumPages()

	print 'Number of pages: '
	print(number_of_pages)
	print(info)
	author = info.author
	creator = info.creator
	producer = info.producer
	subject = info.subject
	title = info.title
	pdb.set_trace()






# def save_file()

if __name__ =='__main__':
	root_path = os.path.expanduser('~')
	file_path = os.path.join(root_path, 'Desktop', 'Gripper Whips.pdf')
	outpath = os.path.join(root_path, 'Desktop', 'pypdf2_out.pdf')

	rotation = 270
	# creating a pdf File object of original pdf 
	pdfFileObj = open(file_path, 'rb') 

	# creating a pdf Reader object 
	pdfReader = PdfFileReader(pdfFileObj) 

	# creating a pdf writer object for new pdf 
	pdfWriter = PdfFileWriter() 

	# rotating each page 
	for page in range(pdfReader.numPages): 
		# creating rotated page object 
		pageObj = pdfReader.getPage(page) 
		pageObj.rotateClockwise(rotation) 
		# adding rotated page object to pdf writer 
		pdfWriter.addPage(pageObj) 
  
	# new pdf file object 
	newFile = open(outpath, 'wb') 

	# writing rotated pages to new file 
	pdfWriter.write(newFile) 

	# closing the original pdf file object 
	pdfFileObj.close() 

	# closing the new pdf file object 
	newFile.close() 





	# #open pdf file
	# with open (file_path, 'rb') as infile:
	# 	pdfReaderObj = PdfFileReader(infile)
	# 	num_pages = pdfReaderObj.getNumPages()
	# 	pages = [pdfReaderObj.getPage(k) for k in range(num_pages)]
	# 	pdb.set_trace()
		



	# outpath = os.path.join(root_path, 'Desktop', 'pypdf2_out.pdf')
	# # get_info(file_path)

	# pdb.set_trace()
	# #create a pdf writer
	# mypdfwriter = PdfFileWriter()

	# #add a page to it
	# mypdfwriter.addPage(pages[1])

	# #open the file object
	# outfile = open(outpath, 'wb')
	
	# #write to the file object
	# mypdfwriter.write(outfile)

	# #close the file object
	# outfile.close()
	# infile.close()
	
	# outfile.close()


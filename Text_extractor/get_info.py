"""Module GetInfo, searches for author, page range, title, publisher,
	year in the given article. Saves everything in a text out_info.txt
	get_info(pdf_file, txt_file) get all the info from the first page of 'pdf_file'.pdf and save it to 'txt_file'.txt 
	"""

import sys
import os
import re
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfpage_mod import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter
from Paper import Paper

def get_info(pdf_file, txt_file):

	laparams = LAParams()
	pagenos = set()
	rsrcmgr = PDFResourceManager(caching = True)

	outtype = 'text'
 	pages_to_extract = 1
	current_page = 0
	temp_author = None

	fp = file(pdf_file, 'rb')
	file_name = txt_file[:-3]+'firstpage.txt'
	out_file = file(file_name,'w')

	device = TextConverter(rsrcmgr, out_file, codec = 'utf-8', laparams=laparams, imagewriter = None)
	interpreter = PDFPageInterpreter(rsrcmgr, device)

	paper = Paper()
	paper.set_pages(PDFPage.get_num(fp, pagenos, maxpages = pages_to_extract, password = '', caching = True, check_extractable = True))
	laparams = LAParams()	
	rsrcmgr = PDFResourceManager(caching = True)

	for page in PDFPage.get_pages(fp, pagenos, maxpages = pages_to_extract, password = '', caching = True, check_extractable = True):
		page.rotate = (page.rotate) % 360
		interpreter.process_page(page)

	out_file.close()
	fp.close()
	device.close()
	
	paper.set_author(find_author(file_name))
	paper.set_page_range(find_range(file_name))
	paper.set_doi(find_doi(file_name))
	line = author_line_num(file_name)
	paper.set_title(find_title(file_name, line))
	paper.set_year(find_year(file_name))
	paper.set_publisher(find_publisher(file_name))

	os.remove(file_name)

	"""
	info_filename = txt_file[:-3]+'info.txt'
 	paper.generate_citations(info_filename)
 		"""

 	return paper

"""	Find all the authors for a given article
	"""
def find_author(fpt):

	i = 0
	num = 0
	author_arr = set()
	author_duplicates = []

	regex = r"((([A-Z][a-z]+)|([A-Z]\.))\s+(([A-Z]\.)|([A-Z][a-z]+))\s*(([A-Z][a-z]+)|(\,)))"
	with open(fpt) as f:
   			for line in f:
				author = re.findall(regex, line)
				num = num + 1
				if author:
					for i in range(0, len(author)):
						if author[i][0] not in author_arr:
							author_arr.add(author[i][0])
						else:
							author_duplicates.append(author[i][0])

	for name in author_duplicates:
		if name in author_arr:
			author_arr.remove(name)
	f.close()
	return author_arr


""" Get the line number for authors, used in the title search
	"""
def author_line_num(fpt):

	i = 0
	num = 0
	author_line = 0

	regex = r"((([A-Z][a-z]+)|([A-Z]\.))\s+(([A-Z]\.)|([A-Z][a-z]+))*\s*(([A-Z][a-z]+)|(\,)))"
	with open(fpt) as f:
   			for line in f:
				author = re.findall(regex, line)
				num = num + 1
				if author:
					if author_line == 0:
						author_line = num-1
	f.close()
	return author_line


""" Find the year of publication
	"""
def find_year (fpt):

	year_arr = 0
	regex = r"(?:19[7-9]\d|2\d{3})(?=\D|$)"
	with open (fpt) as f:
		for line in f:
			year = re.search (regex, line)
			if year:
				year_arr = year.group(0)
                                       
	f.close()
	return year_arr


""" Find the range of pages in the journal for a given article
	"""
def find_range (fpt):

	pages_arr = None
	regex = r"([0-9]+-[0-9]+)"
	with open (fpt) as f:
		for line in f:
			pages = re.search (regex, line)
			if pages:
				pages_arr = pages.group(0)
				break             
	f.close()
	return pages_arr


""" Find the title on the first page.
	Title is defined as 3 lines right before the authors
	"""
def find_title (fpt, line_num):

	title_arr = ''
	i = 0
	title = [None] * 3
	with open (fpt) as f:
		for line in f: 
			if(len(line)>1):
				title[(i)%3] = line	
			i+=1
			if i == line_num:
				break
	for i in range (i-1, i+2):
		if(title[i%3]):
			title_arr += title[i%3]

	f.close()
	return title_arr	


""" Find the DOI on the first page 
	"""
def find_doi (fpt):

	doi_arr = None
	regex = r"(doi.*)"
	with open (fpt) as f:
		for line in f:
			doi = re.search (regex, line, re.IGNORECASE)
			if doi:
				doi_arr = doi.group(0)
				break            
	f.close()
	return doi_arr

def find_publisher (fpt):

	publisher = None
	regex = r"(Published(.\D)*|.*Journal(.\D)*)"
	with open (fpt) as f:
		for line in f:
			doi = re.search (regex, line, re.IGNORECASE)
			if doi:
				publisher = doi.group(0)
				break            
	f.close()
	return publisher

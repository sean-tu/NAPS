"""Module GetInfo, searches for author, page range, title, publisher,
	year in the given article. Saves everything in a text out_info.txt
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

def get_info(txt_file, page, paper):

	info_filename = txt_file[:-3]+'info.txt'
	laparams = LAParams()	
	rsrcmgr = PDFResourceManager(caching = True)
	file_name = txt_file[:-3]+'firstpage.txt'
	out_file = file(file_name,'w')
	doi_out = TextConverter(rsrcmgr, out_file, codec = 'utf-8', laparams=laparams, imagewriter = None)
	interpreter_doi = PDFPageInterpreter(rsrcmgr, doi_out)

	interpreter_doi.process_page(page)
	out_file.close()
	
	paper.set_author(find_author(file_name))
	paper.set_page_range(find_range(file_name))
	paper.set_doi(find_doi(file_name))
	line = author_line_num(file_name)
	paper.set_title(find_title(file_name, line))
	paper.set_year(find_year(file_name))

 	paper.generate_citations(info_filename)
 	doi_out.close()

 	return 1

def find_author(fpt):

	i = 0
	num = 0
	author_arr = []

	regex = r"((([A-Z][a-z]+)|([A-Z]\.))\s+(([A-Z]\.)|([A-Z][a-z]+))*\s*(([A-Z][a-z]+)|(\,)))"
	with open(fpt) as f:
   			for line in f:
				author = re.findall(regex, line)
				num = num + 1
				if author:
					for i in range(0, len(author)):
						if(len(author_arr)==0):
							author_arr.append(author[i][0])
						elif(author_arr[len(author_arr)-1]!=author[i][0]):
							author_arr.append(author[i][0])
	f.close()
	return author_arr

def author_line_num(fpt):

	i = 0
	num = 0
	author_line = 0

	regex = r"((([A-Z][a-z]+)|([A-Z]\.))\s+(([A-Z]\.)|([A-Z][a-z]+))\s*(([A-Z][a-z]+)|(\,)))"
	with open(fpt) as f:
   			for line in f:
				author = re.findall(regex, line)
				num = num + 1
				if author:
					if author_line == 0:
						author_line = num-1
	f.close()
	return author_line

def find_year (fpt):

	year_arr = []
	regex = r"(?:19[7-9]\d|2\d{3})(?=\D|$)"
	with open (fpt) as f:
		for line in f:
			year = re.search (regex, line)
			if year:
				year_arr = year.group(0)
                                       
	f.close()
	return year_arr

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

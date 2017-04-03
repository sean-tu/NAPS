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
from Metadata import Metadata

def get_info(txt_file, page, paper):

	search_eng = Metadata()
	info_filename = txt_file[:-3]+'info.txt'
	laparams = LAParams()	
	rsrcmgr = PDFResourceManager(caching = True)
	file_name = txt_file[:-3]+'firstpage.txt'
	out_file = file(file_name,'w')
	doi_out = TextConverter(rsrcmgr, out_file, codec = 'utf-8', laparams=laparams, imagewriter = None)
	interpreter_doi = PDFPageInterpreter(rsrcmgr, doi_out)

	interpreter_doi.process_page(page)
	out_file.close()
	search_eng.find_author(file_name)
	paper.set_author(search_eng.author)
	search_eng.find_year(file_name)
	paper.set_year(search_eng.year)
	search_eng.find_range(file_name)
	paper.set_page_range(search_eng.pages)

 	paper.generate_citations(info_filename)
 	doi_out.close()

 	return 1
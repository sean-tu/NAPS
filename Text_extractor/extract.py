"""Modude to extract the text from the pdf.
	extract(pdf, txt) - extracts first 5 pages of the 'pdf_file'.pdf to 'txt_file'.txt
	"""

import sys
import os
import re
from get_info import get_info
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

def extract(pdf_file, txt_file):

  laparams = LAParams()
  pagenos = set()
  rsrcmgr = PDFResourceManager(caching = True)

  outtype = 'text'
  pages_to_extract = 5
  current_page = 0
  temp_author = None

  outfp = file(txt_file, 'w')
  fp = file(pdf_file, 'rb')

  device = TextConverter(rsrcmgr, outfp, codec = 'utf-8', laparams=laparams, imagewriter = None)
  interpreter = PDFPageInterpreter(rsrcmgr, device)

  for page in PDFPage.get_pages(fp, pagenos, maxpages = pages_to_extract, password = '', caching = True, check_extractable = True):
    page.rotate = (page.rotate) % 360
    
    interpreter.process_page(page)

  fp.close()
  device.close()
  outfp.close()
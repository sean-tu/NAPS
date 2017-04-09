"""Modude to extract the text from the pdf.
	extract(pdf, txt) - extracts first 4 pages and the last one from the pdf to txt
	search(filename)  - determines if the page needs to be included base on the presence of citations
	*commented out - debugging and doi output
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
  paper = Paper()
  rsrcmgr = PDFResourceManager(caching = True)

  outtype = 'text'
  pages_to_extract = 5
  current_page = 0
  temp_author = None

  outfp = file(txt_file, 'w')
  fp = file(pdf_file, 'rb')

  device = TextConverter(rsrcmgr, outfp, codec = 'utf-8', laparams=laparams, imagewriter = None)
  interpreter = PDFPageInterpreter(rsrcmgr, device)
  paper.set_pages(PDFPage.get_num(fp, pagenos, maxpages = pages_to_extract, password = '', caching = True, check_extractable = True))

  for page in PDFPage.get_pages(fp, pagenos, maxpages = pages_to_extract, password = '', caching = True, check_extractable = True):
    page.rotate = (page.rotate) % 360
    """
    if current_page == 0:
      current_page += get_info(txt_file,page, paper)
    """
    interpreter.process_page(page)
    

  """
  counter = 1
  found = 0
  pagenos.add(paper.get_pages()-counter)
  while found!=1 or counter>=paper.get_pages():
    for page in PDFPage.get_pages(fp, pagenos, maxpages = 1, password = '', caching = True, check_extractable = True):
      buffer_out_file = file('buffer.txt','w')
      buffer_out = TextConverter(rsrcmgr, buffer_out_file, codec = 'utf-8', laparams=laparams, imagewriter = None)
      interpreter_buffer = PDFPageInterpreter(rsrcmgr, buffer_out)
      page.rotate = (page.rotate)%360
      interpreter_buffer.process_page(page)
      buffer_out_file.close()
      buffer_out.close()
      found = search('buffer.txt')
      if(found!=1):
        counter+=1
        pagenos.add(paper.get_pages()-counter)
      elif found==1:
        interpreter.process_page(page)
    if counter >= paper.get_pages():
        break
  os.remove('buffer.txt')
  """
  fp.close()
  device.close()
  outfp.close()

def search(filename):

  reg = r"(references)"
  with open(filename) as f:
          for line in f:
            if(re.search(reg, line, re.IGNORECASE)):
              return 1
"""Modude to extract the text from the pdf.
	extract(pdf, txt) - extracts first 4 pages and the last one from the pdf to txt
	search(filename)  - determines if the page needs to be included base on the presence of citations
	*commented out - debugging and doi output
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

def extract(pdf_file, txt_file):

  laparams = LAParams()
  pagenos = set()
  paper = Paper()
  search_eng = Metadata()
  rsrcmgr = PDFResourceManager(caching = True)

  outtype = 'text'
  pages_to_extract = 4
  current_page = 0
  temp_author = None
  doi_file_name = txt_file[:-3]+'doi.txt'
  info_filename = txt_file[:-3]+'info.txt'

  outfp = file(txt_file, 'w')
  fp = file(pdf_file, 'rb')

  device = TextConverter(rsrcmgr, outfp, codec = 'utf-8', laparams=laparams, imagewriter = None)
  interpreter = PDFPageInterpreter(rsrcmgr, device)

  """
  doi_out_file = file(doi_file_name,'w')
  doi_out = TextConverter(rsrcmgr, doi_out_file, codec = 'utf-8', laparams=laparams, imagewriter = None)
  interpreter_doi = PDFPageInterpreter(rsrcmgr, doi_out)
  """

  paper.set_pages(PDFPage.get_num(fp, pagenos, maxpages = pages_to_extract, password = '', caching = True, check_extractable = True))

  for page in PDFPage.get_pages(fp, pagenos, maxpages = pages_to_extract, password = '', caching = True, check_extractable = True):
    page.rotate = (page.rotate) % 360
    """ So here the extraction of metadata takes place
        if the page == 0, which is the first one, it tries to extract everything
        However, since pdf's are formatted differently, and the first page is not sufficient,
        we need to restart the counter to 0, and get the next page to do the same procedure.
        Still needs work.
        """
    """
    if current_page == 0:
      interpreter_doi.process_page(page)
      current_page+=1
      doi_out_file.close()
      search_eng.find_author(doi_file_name)
      paper.set_author(search_eng.author)
      search_eng.find_year(doi_file_name)
      paper.set_year(search_eng.year)
      search_eng.find_range(doi_file_name)
      paper.set_page_range(search_eng.pages)
    """
    interpreter.process_page(page)

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
  os.remove('buffer.txt')
  fp.close()
  device.close()
  
  """
  paper.generate_citations(info_filename)
  doi_out.close()
  doi_out_file.close()
  """
  outfp.close()

def search(filename):

  reg = r"(references)"
  with open(filename) as f:
          for line in f:
            if(re.search(reg, line, re.IGNORECASE)):
              return 1
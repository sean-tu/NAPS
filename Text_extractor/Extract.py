import sys
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
  pages_to_extract = 5
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
    """
    interpreter.process_page(page)
  fp.close()
  device.close()
  
  """
  paper.printinfo(info_filename)
  doi_out.close()
  doi_out_file.close()
  """
  outfp.close()
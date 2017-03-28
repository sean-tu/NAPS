"""Slightly modified pdf2txt.py script from PDFMiner library
   Extracts first 5 pages of the pdf, which is fed to the commandline.
   Ex: -pdf2txt input.pdf
   outputs first 5 pages into output.txt
   **Still needs cleaning and the ability to extract the last page. working on it
"""
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

# main
def main(argv):
    import getopt
    def usage():
        print ('usage: %s [-p pagenos] [-m maxpages] [-o output]'
               ' file ...' % argv[0])
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'dp:m:P:o:CnAVM:L:W:F:Y:O:R:t:c:s:')
    except getopt.GetoptError:
        return usage()
    if not args: return usage()
    # debug option
    debug = 0
    # input option
    password = ''
    pagenos = set()
    maxpages = 5
    # output option
    outfile = 'output.txt'
    outtype = 'text'
    imagewriter = None
    rotation = 0
    layoutmode = 'normal'
    codec = 'utf-8'
    pageno = 1
    scale = 1
    caching = True
    showpageno = True
    laparams = LAParams()
    for (k, v) in opts:
        if k == '-p': pagenos.update( int(x)-1 for x in v.split(',') )
        elif k == '-m': maxpages = int(v)
        elif k == '-o': outfile = v

    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFResourceManager.debug = debug
    PDFPageInterpreter.debug = debug
    PDFDevice.debug = debug
    #
    rsrcmgr = PDFResourceManager(caching=caching)
    current_page = 0

    doi_out_file = file('doi.txt','w')
    if outfile:
        outfp = file(outfile, 'w')
    else:
        outfp = sys.stdout

    """device class for the general extraction and the extraction of the doi
    """
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                               imagewriter=imagewriter)
    doi_out = TextConverter(rsrcmgr, doi_out_file, codec=codec, laparams=laparams,
                               imagewriter=imagewriter)

    paper = Paper()
    search_eng = Metadata()
    temp_author = None

    for fname in args:
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        interpreter_doi = PDFPageInterpreter(rsrcmgr, doi_out)

        fp = file(fname, 'rb')
        paper.set_pages(PDFPage.get_num(fp, pagenos,
                                      maxpages=maxpages, password=password,
                                      caching=caching, check_extractable=True))

        for page in PDFPage.get_pages(fp, pagenos,
                                      maxpages=maxpages, password=password,
                                      caching=caching, check_extractable=True):
            page.rotate = (page.rotate+rotation) % 360

            """ So here the extraction of metadata takes place
                if the page == 0, which is the first one, it tries to extract everything
                However, since pdf's are formatted differently, and the first page is not sufficient,
                we need to restart the counter to 0, and get the next page to do the same procedure.
                Still needs work.
                """
            if current_page == 0:
                interpreter_doi.process_page(page)
                current_page+=1
                doi_out_file.close()
                search_eng.find_author('doi.txt')
                paper.set_author(search_eng.author)
            interpreter.process_page(page)
        fp.close()

    paper.printinfo()
    device.close()
    outfp.close()
    return

if __name__ == '__main__': sys.exit(main(sys.argv))

"""
Gets all of the pdf files from the subfolders of a specified folder
"""

import os
from classification.corpus import Corpus, Document
from Text_extractor.Extract import extract

__author__ = "Johnathan Sattler"

Relative_Path = os.path.dirname(os.path.realpath(__file__))

pdf_extension = "pdf"
txt_extension = "txt"


# returns all direct subfolders of the path folder
def get_subfolders(path="papers"):
    folders = []

    final_path = "{}/{}".format(Relative_Path, path)

    sub_folders = [d for d in os.listdir(final_path) if os.path.isdir(os.path.join(final_path, d))]

    for folder in sub_folders:
        folders.append("{}/{}".format(path, folder))

    return folders;
# end get_subfolders


# returns all pdfs in the path folder
def get_pdfs(path="papers"):
    pdfs = []

    for pdf in os.listdir("{}/{}".format(Relative_Path, path)):
        if pdf.endswith(".{}".format(pdf_extension)):
            pdfs.append("{}/{}".format(path, pdf))

    return pdfs
# end get_pdfs


# return all pdfs in the subfolders of the path folder
def batch_extract(path="papers"):
    classifier = Corpus();

    for folder in get_subfolders(path):
        for pdf in get_pdfs(folder):
            folder_name = folder.split("/")[1]
            txt = pdf.replace(".{}".format(pdf_extension), ".{}".format(txt_extension))

            if not os.path.isfile(txt):
                extract(pdf, txt)

            newdoc = Document(path=txt, class_label=folder_name)
            classifier.add_document(document=newdoc)
# end batch_extract

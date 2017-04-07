"""
Gets all of the pdf files from the subfolders of a specified folder
"""

import os
from collections import OrderedDict

from prettytable import PrettyTable

from Text_extractor.extract import extract
import cPickle as pickle

__author__ = "Johnathan Sattler"

Relative_Path = os.path.dirname(os.path.realpath(__file__))

pdf_extension = "pdf"
txt_extension = "txt"


# returns all direct subfolders of the path folder
def get_subfolders(path="papers"):
    folders = []

    final_path = "{}/{}".format(Relative_Path, path)
    print final_path
    sub_folders = [d for d in os.listdir(final_path) if os.path.isdir(os.path.join(final_path, d))]

    for folder in sub_folders:
        folders.append("{}/{}".format(path, folder))

    return folders
# end get_subfolders


# returns all pdfs in the path folder
def get_pdfs(path="papers"):
    pdfs = []

    for pdf in os.listdir("{}/{}".format(Relative_Path, path)):
        if pdf.endswith(".{}".format(pdf_extension)):
            pdfs.append("{}/{}".format(path, pdf))

    return pdfs
# end get_pdfs


# extracts text from all pdfs in the subfolders of the path folder
def batch_extract(path="papers"):
    extracted = 0

    for folder in get_subfolders(path):
        for pdf in get_pdfs(folder):
            txt = pdf.replace(".{}".format(pdf_extension), ".{}".format(txt_extension))

            if not os.path.isfile(txt):
                extract(pdf, txt)
                extracted += 1

    return extracted
# end batch_extract


# creates document for all text files in the subfolders of the path folder
def build_doc_set(path="papers"):
    docs = []

    for folder in get_subfolders(path):
        for pdf in get_pdfs(folder):
            folder_name = folder.split("/")[2]  # CHECK
            txt = pdf.replace(".{}".format(pdf_extension), ".{}".format(txt_extension))

            docs.append((txt, folder_name))

    return docs

# OBJECT PERSISTENCE


def save_object(obj, path):
    with open(path, 'wb') as fout:
        pickle.dump(obj, fout)


def load_object(path):
    with open(path, 'rb') as fin:
        return pickle.load(fin)


# PRINT FUNCTIONS


def print_features(doc):
    features = sort_dictionary(doc.get_features())
    print 'Doc: %s, %d features' % (doc.path, len(features))
    table = PrettyTable(['Token', 'Frequency'])
    table.align = 'l'
    for t, f in features.iteritems():
        table.add_row([t, f])
    print table


def print_docset(docs):
    t = PrettyTable(['Path', 'Category'])
    t.align = 'l'
    for d in docs:
        t.add_row([d.class_label, d.path])
    print t

# DICTIONARY FUNCTIONS


def sort_dictionary(d):
    """ Sorts dictionary in descending order of values 

    >>> sort_dictionary({'lots': 20, 'none': 0, 'few': 2, 'some': 5})
    OrderedDict([('lots', 20), ('some', 5), ('few', 2), ('none', 0)])
    """
    ordered = OrderedDict(sorted(d.items(), key=lambda t: t[1], reverse=True))
    return ordered


if __name__ == '__main__':
    pathname = raw_input("Root folder for batch extraction: ")
    docs = batch_extract(pathname)

    f = raw_input("Pickle file name: ")
    save_object(docs, f)

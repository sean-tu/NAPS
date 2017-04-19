"""
Gets all of the pdf files from the subfolders of a specified folder
"""

import os
import sys
import cPickle as pickle

from collections import OrderedDict
from prettytable import PrettyTable
from Text_extractor.extract import extract
from NAPS.settings import STATIC_ROOT

# to fix pickle module location problem
from . import classifier 
import corpus
import naivebayes
sys.modules['classifier'] = classifier
sys.modules['corpus'] = corpus
sys.modules['naivebayes'] = naivebayes

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
        folder_name = os.path.basename(os.path.normpath(folder))

        for pdf in get_pdfs(folder):
            txt = pdf.replace(".{}".format(pdf_extension), ".{}".format(txt_extension))

            # print "Category: " + folder_name
            # print "Subcategory: "
            # print "PDF File: " + pdf
            # print "TXT File: " + txt + "\n"

            if not os.path.isfile(txt):
                extract(pdf, txt)
                extracted += 1

        for subfolder in get_subfolders(os.path.join(path, folder_name)):
            # subfolder_name = os.path.basename(os.path.normpath(sub_folder))

            for pdf in get_pdfs(subfolder):
                txt = pdf.replace(".{}".format(pdf_extension), ".{}".format(txt_extension))

                # print "Category: " + folder_name
                # print "Subcategory: " + subfolder_name
                # print "PDF File: " + pdf
                # print "TXT File: " + txt + "\n"

                if not os.path.isfile(txt):
                    extract(pdf, txt)
                    extracted += 1

    return extracted
# end batch_extract


# creates document for all text files in the subfolders of the path folder
def build_doc_set(path="papers"):
    batch_extract(path)
    docs = []

    for folder in get_subfolders(path):
        folder_name = os.path.basename(os.path.normpath(folder))

        for pdf in get_pdfs(folder):
            txt = pdf.replace(".{}".format(pdf_extension), ".{}".format(txt_extension))

            # print "Category: " + folder_name
            # print "Subcategory: "
            # print "PDF File: " + pdf
            # print "TXT File: " + txt + "\n"

            docs.append((txt, folder_name, ''))

        for subfolder in get_subfolders(os.path.join(path, folder_name)):
            subfolder_name = os.path.basename(os.path.normpath(subfolder))

            for pdf in get_pdfs(subfolder):
                txt = pdf.replace(".{}".format(pdf_extension), ".{}".format(txt_extension))

                # print "Category: " + folder_name
                # print "Subcategory: " + subfolder_name
                # print "PDF File: " + pdf
                # print "TXT File: " + txt + "\n"

                docs.append((txt, folder_name, subfolder_name))

    return docs

# OBJECT PERSISTENCE


def save_object(obj, path):
    with open(os.path.join(STATIC_ROOT, path), 'wb') as fout:
        pickle.dump(obj, fout)


def load_object(path):
    with open(os.path.join(STATIC_ROOT, path), 'rb') as fin:
        return pickle.load(fin)


# PRINT FUNCTIONS
separator = '\n############\n'


def print_doc(doc):
    print separator, 'Doc: %s, %s' % (doc.path, doc.get_labels())
    print_features(doc.get_features())


def print_features(f):
    features = sort_dictionary(f)
    table = PrettyTable(['Token %d' % len(features), 'Frequency'])
    table.align = 'l'
    for t, f in features.iteritems():
        table.add_row([t, f])
    print table


def compare_features(feat1, feat2):
    """See feature sets side by side"""
    feat1 = sort_dictionary(feat1)
    feat2 = sort_dictionary(feat2)  # this must be the smaller dictionary
    table = PrettyTable(['t1', 'f1', 't2', 'f2'])
    table.align = 'l'
    size = len(feat2)
    print size
    for i in range(size):
        (t1, f1) = feat1.popitem()
        (t2, f2) = feat2.popitem()
        table.add_row([t1, f1, t2, f2])
    print table


def print_docset(docs):
    t = PrettyTable(['Path', 'Category', 'Subcategory'])
    t.align = 'l'
    for d in docs:
        t.add_row([d.path, d.class_label, d.subclass_label])
    print separator, 'DOCSET (%d docs)' % len(docs)
    print t


def print_corpus(corpus):
    table = PrettyTable(['Class', 'Subclass', 'Doc'])
    table.align = 'l'
    for c in corpus.get_classes():
        class_label = c.get_label()
        for s in c.get_classes():
            subclass_label = s.get_label()
            for d in s.documents:
                table.add_row([class_label, subclass_label, d.path])
    print separator, 'CORPUS (%d docs, %d classes)' % (corpus.num_docs, len(corpus.classes))
    print table


def print_errors(errors):
    header = ['Actual', 'Predicted', 'Path']
    t = PrettyTable(header)
    t.align = 'l'
    for e in errors:
        t.add_row(e)
    print t

# DICTIONARY FUNCTIONS


def sort_dictionary(d):
    """ Sorts dictionary in descending order of values 

    >>> sort_dictionary({'lots': 20, 'none': 0, 'few': 2, 'some': 5})
    OrderedDict([('lots', 20), ('some', 5), ('few', 2), ('none', 0)])
    """
    return OrderedDict(sorted(d.items(), key=lambda t: t[1], reverse=True))


def alphabetize_dictionary(d):
    return OrderedDict(sorted(d.items(), key=lambda v: v[0]))


def combine_features(set1, set2):
    """Combines the {feature: value} pairs of two dictionaries

    >>> combine_features({'a':1, 'b':1, 'c':1}, {'a':5, 'b':1, 'd':1}) == {'a':6, 'b':2, 'c':1, 'd':1}
    True

    Result is accumulated in set1 (first parameter), set2 is unchanged
    """
    for f, v in set2.iteritems():
        if f in set1:
            set1[f] += v
        else:
            set1[f] = v
    return set1


if __name__ == '__main__':
    pass


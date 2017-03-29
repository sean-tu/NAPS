"""
Gets all of the pdf files from the specified folder and every subfolder
"""

import os

__author__ = "Johnathan Sattler"

Relative_Path = os.path.dirname(os.path.realpath(__file__))


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

    extension = "pdf"

    for pdf in os.listdir("{}/{}".format(Relative_Path, path)):
        if pdf.endswith(".{}".format(extension)):
            pdfs.append("{}/{}".format(path, pdf))

    return pdfs
# end get_pdfs


# return all pdfs in the path folder, and all of its subfolders
def batch_extract(path="papers"):
    files = []

    pdfs = get_pdfs(path)

    folders = get_subfolders(path)

    for pdf in pdfs:
        files.append(pdf)

    for folder in folders:
        files.extend(batch_extract(folder))

    return files
# end batch_extract

for pdf in batch_extract("papers"):
    print pdf

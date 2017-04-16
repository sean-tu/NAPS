"""These classes define the structure of the corpus

Documents contain information needed for classification and the class_label property which the classifier assigns
Classes contain Documents with a common class_label
The Corpus contains the set of Classes and their associated Documents
"""

import pickle

from prettytable import PrettyTable


class Document:
    def __init__(self, path=None, raw_text=None, class_label='', subclass_label=''):
        self.path = path                # path to text file
        self.raw_text = raw_text        # string of text from text file
        self.tokens = None              # list of tokens from text [token]
        self.features = None            # set of features [(token, frequency)]
        self.class_label = class_label  # name of assigned category
        self.subclass_label = subclass_label

    # Getters/setters
    def set_tokens(self, tokens):
        self.tokens = tokens

    def get_tokens(self):
        return self.tokens

    def set_features(self, features):
        self.features = features

    def get_features(self):
        return self.features

    def get_labels(self):
        return [self.class_label, self.subclass_label]

    def set_labels(self, label, sub_label):
        self.class_label = label
        self.subclass_label = sub_label

    # NOTE: may change to ref containing 'Class' class
    # NOTE: that might get confusing. When OO and classification/ML lingo collide!
    def set_label(self, label):
        self.class_label = label
        # TODO change class if containing class.class_label != class_label

    def __str__(self):
        return self.path

class Corpus:
    """Contains the documents known to the classifier. 

    Documents are organized by class. The Classifier uses the documents' features to calculate class probabilities.
    """

    def __init__(self, level=0):
        self.num_docs = 0
        self.classes = []
        self.vocabulary = {}        # {token: [token_frequency, document_frequency]}
        self.level = level

    def get_classes(self):
        return sorted(self.classes, key=lambda c: c.get_label())

    def get_vocabulary(self):
        return self.vocabulary

    def add_doc(self, doc):
        """Add a document to the corpus with the given class label.
        
        If not specified, document will be given 'uncategorized' label. 
        If corpus does not contain class with that label, create one."""
        self.num_docs += 1
        combine_features(self.vocabulary, doc.get_features())
        if self.level < 2:
            label = doc.get_labels()[self.level]
            c = self.get_class(label)
            c.add_doc(doc)

    def get_class(self, label):
        """Returns Class object with specified class label"""
        for c in self.classes:
            if c.get_label() == label:
                return c
        newclass = Class(label, level=self.level+1)
        self.classes.append(newclass)
        return newclass

    def getN(self):
        """How many docs in class"""
        return self.num_docs

    def __str__(self):
        return 'Corpus (%d docs, %d cats' % (self.num_docs, len(self.classes))


class Class(Corpus):
    """Class of documents (ex: 'Biology') to which a document can be classified."""
    def __init__(self, label, level=1):
        Corpus.__init__(self, level=level)
        self.label = label
        self.documents = []

    def get_class_features(self):
        return self.vocabulary

    def get_label(self):
        return self.label

    def add_doc(self, doc):
        Corpus.add_doc(self, doc)
        self.documents.append(doc)


# Helper function
def combine_features(vocab, new_set):
    """Combines the {feature: value} pairs of two dictionaries

    >>> combine_features({'a':1, 'b':1, 'c':1}, {'a':5, 'b':1, 'd':1}) == {'a':6, 'b':2, 'c':1, 'd':1}
    True
    
    Result is accumulated in set1 (first parameter), set2 is unchanged
    """
    for f,v in new_set.iteritems():
        if f in vocab:
            vocab[f] = [vocab[f][0] + v, vocab[f][1] + 1]
        else:
            vocab[f] = [v, 1]
    return vocab


def main():
    pass

if __name__ == '__main__':
    main()
    # docs = []
    # docs.append(Document(path='a1', class_label='a', subclass_label='1'))
    # docs.append(Document(path='a2', class_label='a', subclass_label='2'))
    # docs.append(Document(path='b1', class_label='b', subclass_label='1'))
    # docs.append(Document(path='b2', class_label='b', subclass_label='2'))
    # docs.append(Document(path='c1', class_label='c', subclass_label='1'))
    # docs.append(Document(path='a2a', class_label='a', subclass_label='2'))
    # corpus = Corpus()
    # for d in docs:
    #     corpus.add_doc(d)
    # utils.print_corpus(corpus)
"""These classes define the structure of the corpus

Documents contain information needed for classification and the class_label property which the classifier assigns
Classes contain Documents with a common class_label
The Corpus contains the set of Classes and their associated Documents
"""

import pickle


class Document:
    def __init__(self, raw_text=None, class_label=None):
        self.raw_text = raw_text
        self.tokens = None
        self.features = None
        self.class_label = class_label

    # Getters/setters
    def set_tokens(self, tokens):
        self.tokens = tokens

    def get_tokens(self):
        return self.tokens

    def set_features(self, features):
        self.features = features

    def get_features(self):
        return self.features

    # NOTE: may change to ref containing 'Class' class
    # NOTE: that might get confusing. When OO and classification/ML lingo collide!
    def set_label(self, label):
        self.class_label = label


class Corpus:
    """Contains the documents known to the classifier

    Documents are organized by class. The Classifier uses the documents' features to calculate class probabilities
    """

    def __init__(self):
        self.num_documents = 0
        self.classes = []

    def add_document(self, document, label='uncategorized'):
        """Add a document to the corpus

        Args:
            document (Document): document to be added
            label (str): the class_label, and hence name of Class which document is assigned
        """
        c = self.get_class(label)
        if not c:
            c = self.Class(label)
            self.classes.append(c)
        c.add_document(document)

    def get_class(self, label):
        for c in self.classes:
            if c.get_label() == label:
                return c
        return None

    def load_corpus(self, path='corpus.pkl'):
        """Populates corpus with documents from pickle file

        Args:
            path (str): file path specifying pickle file from which to load corpus
        """
        with open(path, 'rb') as file_in:
            saved_corpus = pickle.load(file_in)
            self.classes = saved_corpus.classes
            self.num_documents = saved_corpus.num_documents

    def save_corpus(self, path='corpus.pkl'):
        """Save corpus to pickle file"""
        with open(path, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def add_class(self, label):
        class_labels = self.get_class_labels()
        if label not in class_labels:
            new_class = self.Class(label)
            self.classes.append(new_class)

    def get_class_labels(self):
        class_names = []
        for c in self.classes:
            class_names.append(c.get_class_label())
        return class_names

    class Class:
        """Class of documents (ex: 'Biology') to which a document can be classified.

        TODO Will be extended to subclasses later. """
        def __init__(self, label):
            self.class_label = label
            self.documents = []
            self.num_documents = 0

        def add_document(self, document):
            self.documents.append(document)
            self.num_documents += 1

        def get_class_features(self):
            """Combine features dicts of all docs in class"""
            class_features = {}
            for d in self.documents:
                combine_features(class_features, d.get_features())
            return class_features

        def getN(self):
            """How many docs in class"""
            return self.num_documents

        def get_class_label(self):
            return self.class_label

# Helper function
def combine_features(set1, set2):
    """Combines the {feature: value} pairs of two dictionaries

    >>> combine_features({'a':1, 'b':1, 'c':1}, {'a':5, 'b':1, 'd':1})
    {'a':6, 'b':2, 'c':1, 'd':1}

    Result is accumulated in set1 (first parameter), set2 is unchanged
    """
    for f,v in set2.iteritems():
        if f in set1:
            set1[f] += v
        else:
            set1[f] = v
    return set1

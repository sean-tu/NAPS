from Preprocessor import Preprocessor
from FeatureExtractor import FeatureExtractor


class Document:
    def __init__(self, path=None):
        self.tokens = None
        self.features = None
        self.class_label = None
        if path is not None:
            self.path = path

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

    #Documents are organized by class.
    #The Classifier uses the documents' features to calculate class probabilities"""
    def __init__(self):
        self.num_documents = 0
        self.classes = []

    def add_document(self, document, label= 'uncategorized'):
        self.classes[label].add_document(document)
        self.num_documents += 1

    # TODO
    def load_corpus(self, path):
        """Populates corpus with documents"""
        pass

    class Class:
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


def combine_features(set1, set2):
    """Combines the {feature: value} pairs of two dictionaries
    >>> combine_features({'a':1, 'b':1, 'c':1}, {'a':5, 'b':1, 'd':1})
    {'a':6, 'b':2, 'c':1, 'd':1}
    # Result is accumulated in set1 (first parameter), set2 is unchanged
    """
    for f,v in set2.iteritems():
        if f in set1:
            set1[f] += v
        else:
            set1[f] = v
    return set1


def main():
    print "Begin preprocessing"

    # Preprocessor
    path = 'paper1.txt'
    doc1 = Document(path)
    pre = Preprocessor(path)
    pre.filter_tokens()
    tokens = pre.get_tokens()
    print tokens

    # Feature Extractor
    fe = FeatureExtractor(tokens)
    fe.stem_words()
    fe.filter_features()
    print fe



if __name__ == '__main__':
    main()
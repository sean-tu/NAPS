"""These classes define the structure of the corpus

Documents contain information needed for classification and the class_label property which the classifier assigns
Classes contain Documents with a common class_label
The Corpus contains the set of Classes and their associated Documents
"""

import pickle


class Document:
    def __init__(self, path=None, raw_text=None, class_label='uncategorized', subclass_label=''):
        self.path = path                # path to text file
        self.raw_text = raw_text        # string of text from text file
        self.tokens = None              # list of tokens from text
        self.features = None            # set of features (token, frequency)
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

    # NOTE: may change to ref containing 'Class' class
    # NOTE: that might get confusing. When OO and classification/ML lingo collide!
    def set_label(self, label):
        self.class_label = label
        # TODO change class if containing class.class_label != class_label


class Corpus:
    """Contains the documents known to the classifier. 

    Documents are organized by class. The Classifier uses the documents' features to calculate class probabilities.
    """

    def __init__(self):
        self.num_documents = 0
        self.classes = []
        self.vocabulary = {}

    def get_classes(self):
        return sorted(self.classes, key=lambda c: c.get_class_label())

    def get_vocabulary(self):
        return self.vocabulary

    def add_document(self, document):
        """Add a document to the corpus with the given class label.
        
        If not specified, document will be given 'uncategorized' label. 
        If corpus does not contain class with that label, create one."""
        label = document.get_labels()[0]
        c = self.get_class(label)
        if not c:
            c = self.Class(label)
            self.classes.append(c)
        c.add_document(document)
        self.num_documents += 1
        combine_features(self.vocabulary, document.get_features())

    def get_class(self, label):
        """Returns Class object with specified class label"""
        for c in self.classes:
            if c.get_class_label() == label:
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

    # def add_class(self, label):
    #     """Adds class with given label to corpus if it does not already exist."""
    #     class_labels = self.get_class_labels()
    #     if label not in class_labels:
    #         new_class = self.Class(label)
    #         self.classes.append(new_class)

    def get_class_labels(self):
        class_names = []
        for c in self.classes:
            class_names.append(c.get_class_label())
        return class_names

    class Class:
        """Class of documents (ex: 'Biology') to which a document can be classified."""
        # TODO implement subclasses
        def __init__(self, label):
            self.class_label = label
            self.documents = []
            self.num_documents = 0
            self.subclasses = []
            self.features = {}

        def add_document(self, document):
            self.documents.append(document)
            self.num_documents += 1
            combine_features(self.features, document.get_features())
            sub_label = document.subclass_label
            if sub_label != '' and self.class_label != sub_label:
                s = self.get_subclass(sub_label)
                if s is None:
                    s = self.Class(sub_label)
                    self.subclasses.append(s)
                s.add_document(sub_label)

        def get_subclass(self, label):
            for c in self.subclasses:
                if c.get_class_label() == label:
                    return c
            return None

        def get_class_features(self):
            # """Combine features dicts of all docs in class"""
            # class_features = {}
            # for d in self.documents:
            #     combine_features(class_features, d.get_features())
            return self.features

        def getN(self):
            """How many docs in class"""
            return self.num_documents

        def get_class_label(self):
            return self.class_label


# Helper function
def combine_features(set1, set2):
    """Combines the {feature: value} pairs of two dictionaries

    >>> combine_features({'a':1, 'b':1, 'c':1}, {'a':5, 'b':1, 'd':1}) == {'a':6, 'b':2, 'c':1, 'd':1}
    True
    
    Result is accumulated in set1 (first parameter), set2 is unchanged
    """
    for f,v in set2.iteritems():
        if f in set1:
            set1[f] += v
        else:
            set1[f] = v
    return set1


def main():
    pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()
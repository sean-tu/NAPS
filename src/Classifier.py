"""
Implements the classification algorithm to assign a class label to a given document

In: feature set
Out: class label
"""

__author__ = 'Sean Reedy'

from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

class Classifier:

    def __init__(self):
        self.classifier = None

    # TODO
    def load_classifier(self, path):
        """Choose classifier to use for classification from file"""
        pass

    def set_classifier(self, path=None):
        self.classifier = SklearnClassifier(MultinomialNB())

    def classify(self, document):
        """Determine class probabilities of a given document

        Decide conditional probability of classes for a document instance, using the classifier and corpus.
        """
        features = document.get_features()
        probs = self.classifier.prob_classify(features)

        # Select class with maximum probability
        maxP = 0
        label = None
        for C, P in probs:
            if P > maxP:
                label = C
        return label

    def train(self, train_set):
        self.classifier.train([(d.get_features(), d.get_label() ) for d in train_set])

    # TODO
    def test(self, test_set, train_set):
        pass



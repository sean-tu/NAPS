"""
Implements the classification algorithm to assign a class label to a given document

In: document with feature set
Out: class label
"""
from __future__ import division

import random

from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB
from corpus import Corpus
from naivebayes import NaiveBayes
# from sklearn.pipeline import Pipeline

__author__ = 'Sean Reedy'


class Classifier:

    def __init__(self):
        self.classifier = None
        self.corpus = Corpus()
        self.set_classifier()

    def output_probs(self):
        if isinstance(self.classifier, NaiveBayes):
            self.classifier.output_probs()

    # TODO
    def load_classifier(self, path):
        """Choose classifier to use for classification from file"""
        pass

    def set_classifier(self, path=None):
        if path is None:
            self.classifier = SklearnClassifier(MultinomialNB())

    def classify_probs(self, document):
        """Determine class probabilities of a given document

        Decide conditional probability of classes for a document instance, using the classifier.
        """
        features = document.get_features()
        probs = self.classifier.prob_classify(features)
        return probs

    def classify(self, document):
        """Runs the classifier on a single document and returns the most likely class label."""
        return self.classifier.classify(document.get_features())

    def train(self, train_set):
        """Teaches the classifier with labeled data instances."""
        labeled_feature_set = [(d.get_features(), d.get_label()) for d in train_set]
        print 'Training on %d documents\n' % len(labeled_feature_set)
        for d in train_set:
            self.corpus.add_document(d)
        if isinstance(self.classifier, NaiveBayes):
            self.classifier.train(self.corpus)
        else:
            self.classifier.train(labeled_feature_set)

    def test(self, test_set):
        """Using a new set of documents, tests the accuracy of the classifier. 
        
        # It is important the classifier has not been previously trained on the test set."""
        tested = 0
        correct = 0
        errors = []
        print ('Testing %d documents' % (len(test_set)))
        for actual, predicted in [(d.get_label(), self.classify(d)) for d in test_set]:
            if actual == predicted:
                correct += 1
            else:
                errors.append((predicted, actual))
            tested += 1
        accuracy = float(correct/tested)
        print 'Accuracy=%f, tested=%d, correct=%d, errors=%d' % (accuracy, tested, correct, len(errors))
        return accuracy

    def train_and_test(self, dev_set, split=.5):
        """Splits dev set into training and testing sets then trains/tests
        # split: (0:1) """
        random.shuffle(dev_set)
        s = int(len(dev_set) * split)
        test_set = dev_set[:s]
        train_set = dev_set[s:]
        # if not exclusive(train_set, self.corpus):
          #  print 'ERROR: training set must not be known to classifier!'
        self.train(train_set)
        accuracy = self.test(test_set)
        return accuracy


# Helper functions
def exclusive(set1, set2):
    """Determine if two sets of Documents are exclusive"""
    if set1 is None or set2 is None:
        return True
    for d1 in set1:
        for d2 in set2:
            if d1 == d2:
                return False
    return True


def c_map(probs):
    """Returns the maximum a posteriori class (most likely class) given a set of calculated probabilities."""
    maxP = 0
    label = None
    for C, P in probs.iteritems(): # class C, probability P
        if P > maxP:
            label = C
    return label


def main():
    pass

if __name__ == '__main__':
    main()
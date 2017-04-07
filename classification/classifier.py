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
from prettytable import PrettyTable
# from sklearn.pipeline import Pipeline

__author__ = 'Sean Reedy'


class Classifier:

    def __init__(self):
        self.classifier = None
        self.corpus = Corpus()

    def output_probs(self):
        """Use PrettyTable to print calculated probabilities"""
        if isinstance(self.classifier, NaiveBayes):
            self.classifier.output_probs()

    def set_classifier(self, path=None):
        if path is None:
            path = SklearnClassifier(MultinomialNB())
        self.classifier = path

    def prob_classify(self, document):
        """Determine class probabilities of a given document

        Decide conditional probability of classes for a document instance, using the classifier.
        """
        features = document.get_features()
        probs = self.classifier.prob_classify(features)
        return probs

    def classify(self, document):
        """Runs the classifier on a single document and returns the most likely class label."""
        probs = self.prob_classify(document)
        return self.c_map(probs)

    def c_map(self, probs):
        """Returns the maximum a posteriori class (most likely class) given a set of calculated probabilities."""
        if isinstance(self.classifier, SklearnClassifier): return probs.max()
        maxP = -9999
        label = None
        for C, P in probs:  # class C, probability P
            if P > maxP:
                maxP = P
                label = C
        return label

    def train(self, train_set):
        """Teaches the classifier with labeled data instances.
        sub = 0 : normal 
        sub = 1 : subclasses 
        """
        labeled_feature_set = [(d.get_features(), d.get_labels()[0]) for d in train_set]
        print 'Training on %d documents...\n' % len(labeled_feature_set)
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
        print ('Testing with %d documents...' % (len(test_set)))
        for path, actual, predicted in [(d.path, d.get_labels()[0], self.classify(d)) for d in test_set]:
            if actual == predicted:
                correct += 1
            else:
                errors.append((actual, predicted, path))
            tested += 1
        accuracy = float(correct/tested)
        print 'Accuracy=%f, tested=%d, correct=%d, errors=%d' % (accuracy, tested, correct, len(errors))
        self.print_errors(errors)
        return accuracy

    def print_errors(self, errors):
        header = ['Actual', 'Predicted', 'Path']
        t = PrettyTable(header)
        t.align = 'l'
        for e in errors:
            t.add_row(e)
        print t

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


def main():
    pass

if __name__ == '__main__':
    main()
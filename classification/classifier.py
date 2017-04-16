"""
Implements the classification algorithm to assign a class label to a given document

In: document with feature set
Out: class label
"""
from __future__ import division
import random

from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB

import utils
from corpus import Corpus
from corpus import Document
from naivebayes import NaiveBayes
# from sklearn.pipeline import Pipeline

__author__ = 'Sean Reedy'


class Classifier:

    def __init__(self):
        self.corpus = Corpus()
        self.classifier = None
        self.subclassifiers = {}

    def set_classifier(self, path=None):
        # if path is None:
        #     path = SklearnClassifier(MultinomialNB())
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

    def subclassify(self, document, class_label):
        if class_label not in self.subclassifiers:
            return ''
        subclassifier = self.subclassifiers[class_label]
        probs = subclassifier.prob_classify(document.get_features())
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

    def test(self, test_set):
        """Using a new set of documents, tests the accuracy of the classifier. 
        
        # It is important the classifier has not been previously trained on the test set."""
        tested = 0
        correct = 0
        errors = []
        level = 0   # 0=class, 1=subclass
        print ('Testing with %d documents...' % (len(test_set)))
        for doc in test_set:
            actual = doc.get_labels()   # [class_label, subclass_label]
            p_class = self.classify(doc)
            p_subclass = self.subclassify(doc, actual[0])   # use correct subclassifier for now
            predicted = [p_class, p_subclass]
            if actual[0] == predicted[0]:
                correct += 1
            else:
                errors.append((actual, predicted, doc))
            tested += 1
        accuracy = float(correct/tested)
        print 'Accuracy=%f, tested=%d, correct=%d, errors=%d' % (accuracy, tested, correct, len(errors))
        utils.print_errors(errors)
        return accuracy

    def train(self, train_set):
        """Teaches the classifier with labeled data instances."""
        for d in train_set:
            self.corpus.add_doc(d)
        print 'Training on %d documents...\n' % len(train_set)
        if isinstance(self.classifier, NaiveBayes):
            self.classifier.train(self.corpus)
            for c in self.corpus.get_classes():
                if len(c.get_classes()) > 1:
                    subclassifier = NaiveBayes()
                    subclassifier.train(c)
                    self.subclassifiers[c.get_label()] = subclassifier
        else:   # for nltk classifiers
            labeled_feature_set = [(d.get_features(), d.get_labels()[0]) for d in train_set]
            self.classifier.train(labeled_feature_set)  # Sklearn classifiers

    def train_and_test(self, dev_set, split=.5):
        """Splits dev set into training and testing sets then trains/tests
        # split: (0:1) """
        random.shuffle(dev_set)
        s = int(len(dev_set) * split)
        test_set = dev_set[:s]
        train_set = dev_set[s:]
        self.train(train_set)
        accuracy = self.test(test_set)
        return accuracy

    def output_probs(self):
        """Use PrettyTable to print calculated probabilities"""
        if isinstance(self.classifier, NaiveBayes):
            self.classifier.output_probs()


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
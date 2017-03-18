"""
Implements the classification algorithm to assign a class label to a given document

In: feature set
Out: class label
"""

__author__ = 'Sean Reedy'

from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB
# from sklearn.pipeline import Pipeline


class Classifier:

    def __init__(self):
        self.classifier = None
        self.corpus = None

    # TODO
    def load_classifier(self, path):
        """Choose classifier to use for classification from file"""
        pass

    def set_classifier(self, path=None):
        if path is None:
            self.classifier = SklearnClassifier(MultinomialNB())

    def classify_probs(self, document):
        """Determine class probabilities of a given document

        Decide conditional probability of classes for a document instance, using the classifier and corpus.
        """
        features = document.get_features()
        probs = self.classifier.prob_classify(features)
        return probs

    def classify(self, document):
        probs = self.classify_probs(document)
        label = max_prob(probs)
        return label

    def train(self, train_set):
        self.classifier.train([(d.get_features(), d.get_label() ) for d in train_set])

    def test(self, test_set):
        tested = 0
        correct = 0
        collisions = 0  # number of times a doc in testing set occurs in corpus (bad)
        for d in test_set:
            if d in self.corpus:
                collisions += 1
            if d.get_label == self.classify(d):
                correct += 1
            tested += 1

        print 'Tested=%d, correct=%d, accuracy=%f, collisions=%d' % (tested, correct, correct/tested, collisions)


    def train_and_test(self, dev_set, split=.5):
        """Splits dev set into training and testing sets then trains/tests
        # split: (0:1) """
        s = int(len(dev_set) * split)
        train_set = dev_set[:s]
        test_set = dev_set[:s]
        if not exclusive(train_set, self.corpus):
            print 'ERROR: training set must not be known to classifier!'
        self.train(train_set)
        self.test(test_set)


# Helper functions

def exclusive(set1, set2):
    """Determine if two sets of Documents are exclusive"""
    for d1 in set1:
        for d2 in set2:
            if d1 == d2:
                return False
    return True


def max_prob(probs):
    maxP = 0
    label = None
    for C, P in probs:
        if P > maxP:
            label = C
    return label


def main():
    pass

if __name__ == '__main__':
    main()
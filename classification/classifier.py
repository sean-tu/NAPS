"""
Implements the classification algorithm to assign a class label to a given document

In: document with feature set
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

        Decide conditional probability of classes for a document instance, using the classifier.
        """
        features = document.get_features()
        probs = self.classifier.prob_classify(features)
        return probs

    def classify(self, document):
        """Runs the classifier on a single document and returns the most likely class label."""
        probs = self.classify_probs(document)
        label = probs.max()
        return label

    def train(self, train_set):
        """Teaches the classifier with labeled data instances."""
        labeled_feature_set = [(d.get_features(), d.get_label()) for d in train_set]
        self.classifier.train(labeled_feature_set)

    def test(self, test_set):
        """Using a new set of documents, tests the accuracy of the classifier. 
        
        # It is important the classifier has not been previously trained on the test set."""
        tested = 0
        correct = 0
        collisions = 0  # number of times a doc in testing set occurs in corpus. These docs are ignored.
        errors = []
        print ('Testing %d documents' % (len(test_set)))
        for d in test_set:
            if d in self.corpus:
                collisions += 1
            else:
                prediction = self.classify(d)
                actual = d.get_label()
                if prediction == actual:
                    correct += 1
                else:
                    errors.append((prediction, actual)) # add (prediction, actual) to list of errors
            tested += 1
        accuracy = correct/tested
        print 'Tested=%d, correct=%d, accuracy=%f, collisions=%d' % (tested, correct, accuracy, collisions)
        print 'Errors:'
        for p, a in errors:
            print('Predicted = %s, Actual = %s ' % (p, a))
        return accuracy

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
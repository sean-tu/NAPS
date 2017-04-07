"""Mutlinomial Naive Bayes Classifier"""
from collections import OrderedDict
import math
from prettytable import PrettyTable
from corpus import Corpus

__author__ = 'Sean Reedy'


class NaiveBayes:
    def __init__(self):
        self.alpha = 1          # laplace smoothing
        self.vocabulary = {}    # all tokens in corpus and their frequencies, alphabetized
        self.classes = []       # list of classes, alphabetized
#       self.condprob           # conditional probability of token t given class c
        self.prior = []            # prior probabilities of classes

    def classify(self, document):
        features = document.get_features()
        score = []
        max = 0
        cmap = 0
        for c in range(len(self.classes())):
            score[c] = math.log(self.prior[c])
            for t in features:
                i = self.vocabulary.values().index(t)
                score[c] += math.log(self.condprob[c][i])
            if score[c] > max:
                cmap = c
        return self.classes[cmap].get_class_label()


    def train(self, corpus):
        self.vocabulary = OrderedDict((sorted(corpus.get_vocabulary().items(), key=lambda t: t[0])))
        vocab_length = len(self.vocabulary)     # number of terms in vocabulary
        N = corpus.num_documents
        print '%d Documents\n' % N
        ci = 0   # class counter
        self.classes = corpus.get_classes()
        self.condprob = [[0 for x in range(vocab_length)] for y in range(len(self.classes))]
        for c in self.classes:
            self.prior.append(float(c.getN()) / float(N))
            ti = 0
            class_features = c.get_class_features()
            class_length = sum_features(class_features)
            for t in self.vocabulary:
                if t in class_features:
                    self.condprob[ci][ti] = float(class_features[t] + self.alpha) / float(class_length + vocab_length)
                ti += 1
            ci += 1

    def output_probs(self):
        header = ['Class', 'Prior']
        for k in self.vocabulary.keys():
            header.append(k)
        t = PrettyTable(header)
        i = 0
        for c in self.classes:
            row = [c.get_class_label()]
            row.append(self.prior[i])
            for p in self.condprob[i]:
                row.append(p)
            t.add_row(row)
            i += 1
        print t


# TODO refactor, move these to utils.py
def sum_features(features):
    sum = 0
    for f, v in features.iteritems():
        sum += v
    return sum


def combine_features(set1, set2):
    """Combines the {feature: value} pairs of two dictionaries

    >>> combine_features({'a':1, 'b':1, 'c':1}, {'a':5, 'b':1, 'd':1}) == {'a':6, 'b':2, 'c':1, 'd':1}
    True

    Result is accumulated in set1 (first parameter), set2 is unchanged
    """
    for f, v in set2.iteritems():
        if f in set1:
            set1[f] += v
        else:
            set1[f] = v
    return set1


def sort_dictionary(d):
    """ Sorts dictionary in descending order of values 

    >>> sort_dictionary({'lots': 20, 'none': 0, 'few': 2, 'some': 5})
    OrderedDict([('lots', 20), ('some', 5), ('few', 2), ('none', 0)])
    """
    ordered = OrderedDict(sorted(d.items(), key=lambda t: t[1], reverse=True))
    return ordered
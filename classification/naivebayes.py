"""Mutlinomial Naive Bayes Classifier"""
from collections import OrderedDict
import math
from prettytable import PrettyTable

import utils
from corpus import Corpus

__author__ = 'Sean Reedy'


class NaiveBayes:
    def __init__(self):
        self.alpha = 1          # laplace smoothing
        self.vocabulary = {}    # all tokens in corpus and their frequencies, alphabetized
        self.classes = []       # list of classes, alphabetized
        self.condprob = None    # conditional probability of token t given class c
        self.prior = []         # prior probabilities of classes
        self.N = 0              # number of documents in corpus

    def normalize(self, vector):
        """Transform vector into it's unit vector"""
        u = []      # unit vector = vector/magnitude
        sum = 0     # radicand = (v1^2 + v2^2 + ... + vn^2)
        for v in vector:
            sum += v*v
        magnitude = math.sqrt(sum)  # = sqrt(v1^2 + v2^2 + ... + vn^2)
        for v in vector:
            u.append(float(v) / float(magnitude))
        return u

    def idf(self, term):
        if term in self.vocabulary:

            file = open('pleasework.txt', 'w+')
            file.write(self.vocabulary.get(term))

            #testing??
            #print self.vocabulary.get(term)
            #print self.vocabulary.get(term)[1]
            
            occurences = self.vocabulary.get(term)[1]
        else:
            occurences = 0
        idf = float(self.N) / float(1 + occurences)
        return math.log(idf, 10)

    def tf_idf(self, term):
        """Calculate the term-frequency inverse-document frequency of a term in the vocabulary"""
        if term in self.vocabulary:
            term_freq = self.vocabulary.get(term)[0]
        else:
            term_freq = 0
        return term_freq * self.idf(term)

    def weight_features(self, feature_set, k=.5):
        """Pick k features with highest tfidf weight"""
        split = int(len(feature_set) * k)
        weighted = {}
        for f, v in feature_set.iteritems():
            weighted[f] = v * self.idf(f)
        return dict(sorted(weighted.items(), key=lambda t: t[1], reverse=True)[:split])

    def print_feats(self, features):
        weighted = self.weight_features(features)
        utils.compare_features(features, weighted)

    def prob_classify(self, feature_set):
        # utils.print_vocab(self.vocabulary)
        score = []
        weighted_set = self.weight_features(feature_set)
        for c in range(len(self.classes)):
            score.append(math.log(self.prior[c], 10))
            for t in weighted_set:
                if t in self.vocabulary.keys():
                    i = self.vocabulary.keys().index(t)
                    score[c] += math.log(self.condprob[c][i], 10)
        return zip([c.get_label() for c in self.classes], score)

    def train(self, corpus):
        self.vocabulary = utils.alphabetize_dictionary(corpus.get_vocabulary())
        vocab_length = len(self.vocabulary)     # number of terms in vocabulary
        self.N = corpus.num_docs
        ci = 0   # class counter
        self.classes = corpus.get_classes()
        self.condprob = [[0 for x in range(vocab_length)] for y in range(len(self.classes))]
        for c in self.classes:
            self.prior.append(float(c.getN()) / float(self.N))
            ti = 0
            class_features = c.get_class_features()
            class_length = sum_features(class_features) # TODO fix this to occurences not sum(freqs) maybe
            for t in self.vocabulary:
                freq = 0
                if t in class_features.keys():
                    freq = class_features[t][0]
                self.condprob[ci][ti] = float(freq + self.alpha) / float(class_length + vocab_length/10)
                ti += 1
            ci += 1
        # self.output_probs()

    def output_probs(self):
        print 'Probabilities (%d):' % len(self.vocabulary)
        header = ['Class', 'Prior']
        for k in self.vocabulary.keys():
            header.append(k)
        t = PrettyTable(header)
        t.align = "l"
        i = 0
        for c in self.classes:
            row = [c.get_label()]
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
        sum += v[0]
    return sum


def sort_dictionary(d):
    """ Sorts dictionary in descending order of values 

    >>> sort_dictionary({'lots': 20, 'none': 0, 'few': 2, 'some': 5})
    OrderedDict([('lots', 20), ('some', 5), ('few', 2), ('none', 0)])
    """
    return OrderedDict(sorted(d.items(), key=lambda t: t[1], reverse=True))
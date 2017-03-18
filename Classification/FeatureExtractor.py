""" From a list of tokens, extracts the set of features to be used for classification of a document"""

__author__ = "Sean Reedy"

from nltk.stem import PorterStemmer
from collections import OrderedDict


class FeatureExtractor:
    def __init__(self, tokens):
        self.features = self.featurize(tokens)
        self.stemmer = PorterStemmer()
        self.min_freq = 2   # minimum frequency of token to be considered in classification
        self.weights = []   # maybe later

    # Mutator methods
    def featurize(self, token_list):
        """ Convert list of tokens to a frequency distribution
        # features['word'] = number of times 'word' appears in text """
        features = {}
        for t in token_list:
            if t not in features:
                features[t] = 1
            else:
                features[t] += 1
        return features

    def stem_words(self):
        """ Normalizes word forms using the Porter Stemming algorithm
        Combines features with common stem into one feature
        >>> stem_words({'walk': 3, 'walking': 1, 'walked': 2})
        {'walk': 6}
        """
        stemmed = {}
        for f, v in self.features.iteritems():
            s = self.stemmer.stem(f)
            if s in stemmed:
                stemmed[s] += v
            else:
                stemmed[s] = v
        self.set_features(stemmed)

    def sort_dictionary(self, d):
        """ Sorts dictionary in descending order of values """
        ordered = OrderedDict(sorted(d.items(), key=lambda t: t[1], reverse=True))
        return ordered

    def filter_features(self, min_freq=2):
        features = {}
        for f, v in self.features.iteritems():
            if v >= min_freq:
                features[f] = v
        self.set_features(features)

    # Getters/setters
    def get_features(self):
        return self.features

    def set_features(self, f):
        self.features = f

    def __str__(self):
        separator = '%s\n' % ('#'*12)
        result = separator + 'Features (%d):' % len(self.features) + '\n'
        features = self.sort_dictionary(self.features)
        for f, v in features.iteritems():
            result += '%s - %d' % (f.encode('utf-8'), v) + '\n'
        return result + separator

def main():
    pass

if __name__ == '__main__':
    main()

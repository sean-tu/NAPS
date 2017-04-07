""" From a list of tokens, extracts the set of features to be used for classification of a document"""
# IMPORTANT: There's a bug in nltk/stem/porter.py. Must add 'len(word) >= 2 and' to line 214.

__author__ = "Sean Reedy"

from nltk.stem import PorterStemmer
from collections import OrderedDict


class FeatureExtractor:
    def __init__(self, min_freq=4):
        self.stemmer = PorterStemmer()
        self.min_freq = min_freq        # minimum frequency of token to be considered in classification
        # self.weights = []             # maybe later

    def process(self, tokens):
        f = self.featurize(tokens)
        f = self.stem_words(f)
        f = self.filter_features(f)
        return f

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

    def stem_words(self, features):
        """ Normalizes word forms using the Porter Stemming algorithm.
        
        Given a set of features [(token, freq)], stemming compacts the set by combining tokens with common stems."""
        # TODO Associate tokens with stemmed features
        # TODO investigate other stemming methods
        stemmed = {}
        for f, v in features.iteritems():
            s = self.stemmer.stem(f)
            if s in stemmed:
                stemmed[s] += v
            else:
                stemmed[s] = v
        return stemmed

    def filter_features(self, features):
        """Remove from dictionary items with value smaller than min_freq"""
        delete = []
        for f, v in features.iteritems():
            if v < self.min_freq:
                delete.append(f)
        for f in delete:
            del features[f]
        return features

    # Getters/setters
    def print_features(self, features):
        separator = '%s\n' % ('#'*12)
        result = separator + 'Features (%d):' % len(features) + '\n' # TODO fix length
        features = sort_dictionary(features)
        for f, v in features.iteritems():
            result += '%s - %d' % (f.encode('utf-8'), v) + '\n'
        print result + separator


def sort_dictionary(d):
    """ Sorts dictionary in descending order of values 
    
    >>> sort_dictionary({'lots': 20, 'none': 0, 'few': 2, 'some': 5})
    OrderedDict([('lots', 20), ('some', 5), ('few', 2), ('none', 0)])
    """
    ordered = OrderedDict(sorted(d.items(), key=lambda t: t[1], reverse=True))
    return ordered


# def filter_features(features, min_freq=1):
#     """Remove from dictionary items with value smaller than min_freq
#
#     >>> filter_features({'a':2, 'b':10, 'c':1, 'd':0, 'e':5}, 2) == {'a':2, 'b':10, 'e':5}
#     True
#     """
#     to_remove = []
#     for f, v in features.iteritems():
#         if v < min_freq:
#             to_remove.append(f)
#
#     for i in to_remove:
#         del features[i]
#
#     return features



def main():
    pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # doctest.testmod(extraglobs={'t': Test()})
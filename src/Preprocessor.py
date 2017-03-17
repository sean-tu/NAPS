""" Processes and converts raw text to tokens. This is the first step in the classification process.
It is independent of the classification algorithm.  """

__author__ = 'Sean Reedy'

from nltk import word_tokenize
from nltk.corpus import stopwords

import codecs


class Preprocessor:

    # Constructor
    def __init__(self, path):
        self.raw = self.load_file(path)
        self.tokens = self.tokenize(self.raw)

        self.stopwords = stopwords.words('english')
        self.minLength = 2

    def load_file(self, path):
        """ Read file to string """
        raw = codecs.open(path, 'r', 'utf-8').read()
        return raw

    def tokenize(self, raw):
        """ Convert string to a list of tokens, i.e. individual words """
        raw_tokens = word_tokenize(raw)
        return raw_tokens

    def filter_tokens(self):
        """ Remove non-words, short words (<minLength), and stopwords (common words that don't give information """
        filtered = [w.lower() for w in self.tokens
                    if len(w) > self.minLength
                    and w.isalpha()
                    and w.lower() not in self.stopwords]
        self.tokens = filtered

    # Accessor methods
    def get_tokens(self):
        return self.tokens


def main():
    pass

if __name__ == '__main__':
    main()
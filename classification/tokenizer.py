""" Processes and converts raw text to tokens. This is the first step in the classification process.

It is independent of the classification algorithm.
"""

from nltk import word_tokenize
from nltk.corpus import stopwords
import codecs

__author__ = 'Sean Reedy'


class Tokenizer:
    """Collects unigrams for bag of words style classification and filters out irrelevant tokens."""

    def __init__(self, path):
        """Load raw text input, convert to tokens, and filter out unnecessary tokens."""

        self.raw_text = None
        self.tokens = None

        self.stopwords = stopwords.words('english') # TODO Update with low-information words
        self.MIN_WORD_LENGTH = 2

        self.load_input(path)
        self.tokenize()
        self.filter_tokens()

        # TODO exceptions for failed file loading cases

    def load_input(self, path):
        """ Read file to string """
        f = codecs.open(path, 'r', 'utf-8')
        raw = f.read()
        self.raw_text = raw

    def tokenize(self):
        """Convert string to a list of tokens, i.e. individual words """
        raw_tokens = word_tokenize(self.raw_text)
        self.tokens = raw_tokens

    def filter_tokens(self):
        """Remove non-words, short words (<minLength), and stopwords (common words that don't give information"""
        filtered = [w.lower() for w in self.tokens
                    if len(w) > self.MIN_WORD_LENGTH
                    and w.isalpha()
                    and w.lower() not in self.stopwords]
        self.tokens = filtered

    def get_tokens(self):
        return self.tokens


def main():
    pass

if __name__ == '__main__':
    main()
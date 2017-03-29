""" Processes and converts raw text to tokens. This is the first step in the classification process.

It is independent of the classification algorithm.
"""

from nltk import word_tokenize
from nltk.corpus import stopwords
import codecs

__author__ = 'Sean Reedy'


class Tokenizer:
    """Collects unigrams for bag of words style classification and filters out irrelevant tokens."""

    def __init__(self, min_length=2):
        """Load raw text input, convert to tokens, and filter out unnecessary tokens."""
        self.stopwords = stopwords.words('english') # TODO Update with low-information words
        self.MIN_WORD_LENGTH = min_length

    def load_input(self, path):
        """ Read file to string """
        f = codecs.open(path, 'r', 'utf-8')
        raw_text = f.read()
        return raw_text

    def tokenize(self, raw_text):
        """Convert string to a list of tokens, i.e. individual words """
        # TODO implement
        raw_tokens = word_tokenize(raw_text)
        return self.filter_tokens(raw_tokens)

    def filter_tokens(self, tokens):
        """Remove non-words, short words (<minLength), and stopwords (common words that don't give information"""
        # TODO get hyphenated words
        filtered = [w.lower() for w in tokens
                    if len(w) > self.MIN_WORD_LENGTH
                    and w.isalpha()
                    and w.lower() not in self.stopwords]
        return filtered


def main():
    pass

if __name__ == '__main__':
    main()
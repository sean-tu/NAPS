from Preprocessor import Preprocessor
from FeatureExtractor import FeatureExtractor


class Document:
    def __init__(self, path=None):
        self.tokens = None
        self.features = None
        self.class_label = None
        if path is not None:
            self.path = path

    # Getters/setters
    def set_tokens(self, tokens):
        self.tokens = tokens

    def get_tokens(self):
        return self.tokens

    def set_features(self, features):
        self.features = features

    def get_features(self):
        return self.features


def main():
    print "Begin preprocessing"

    # Preprocessor
    path = 'paper1.txt'
    doc1 = Document(path)
    pre = Preprocessor(path)
    pre.filter_tokens()
    tokens = pre.get_tokens()
    print tokens

    # Feature Extractor
    fe = FeatureExtractor(tokens)
    fe.stem_words()
    fe.filter_features()
    print fe



if __name__ == '__main__':
    main()
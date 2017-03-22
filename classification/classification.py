"""Driver for the classification package."""

from tokenizer import Tokenizer
from feature_extractor import FeatureExtractor
from corpus import Corpus, Document


def main():

    # Tokenizer
    path = 'paper1.txt'
    doc1 = Document(path)
    processor = Tokenizer(path)
    processor.filter_tokens()
    tokens = processor.get_tokens()
    print tokens

    # Feature Extractor
    fe = FeatureExtractor(tokens)
    fe.stem_words()
    fe.filter_features()
    print fe


if __name__ == '__main__':
    main()
"""Driver for the classification package."""
from classifier import Classifier
from tokenizer import Tokenizer
from feature_extractor import FeatureExtractor
from corpus import Corpus, Document


def main():

    # Tokenize
    path = 'ex.txt'
    processor = Tokenizer(path)
    processor.filter_tokens()
    tokens = processor.get_tokens()
    print tokens

    # Extract features
    fe = FeatureExtractor(tokens)
    fe.stem_words()
    fe.filter_features()
    features = fe.get_features()

    # Create document
    doc1 = Document()
    doc1.set_tokens(tokens)
    doc1.set_features(features)

    # Classify


    #Need to train classifier before classifying instances.



if __name__ == '__main__':
    main()

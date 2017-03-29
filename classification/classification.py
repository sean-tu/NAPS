"""Driver for the classification package."""
from classifier import Classifier
from tokenizer import Tokenizer
from feature_extractor import FeatureExtractor
from corpus import Corpus, Document


class Classification:

    # Setup
    def __init__(self):
        self.tokenizer = Tokenizer(min_length=2)
        self.feature_ext = FeatureExtractor(min_freq=2)
        self.classifier = Classifier()

    # Extracts features from raw text
    def process_document(self, doc):
        """Tokenizes new document and extracts its features"""
        if doc.raw_text is None:
            if doc.path:
                doc.raw_text = self.tokenizer.load_input(doc.path)
            # TODO else raise exception
        tokens = self.tokenizer.tokenize(doc.raw_text)
        features = self.feature_ext.process(tokens)
        doc.set_tokens(tokens)
        doc.set_features(features)


def main():
    pass

if __name__ == '__main__':
    main()

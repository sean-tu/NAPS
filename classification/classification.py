"""Driver for the classification package."""
# from classifier import Classifier
from tokenizer import Tokenizer
from feature_extractor import FeatureExtractor
import utils
from corpus import Document
from corpus import Corpus
from classifier import Classifier
from collections import OrderedDict
from naivebayes import NaiveBayes


class Processor:

    # Setup
    def __init__(self):
        self.tokenizer = Tokenizer(min_length=2)
        self.feature_ext = FeatureExtractor(min_freq=2)
        # self.classifier = Classifier()

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


def build_doc_set(path):
    path_list = utils.build_doc_set(path)
    docs = [Document(path=p, class_label=c) for p, c in path_list]
    return docs


def main():
    docs = build_doc_set('../papers')

    driver = Processor()
    corpus = Corpus()
    for d in docs:
        driver.process_document(d)
        # corpus.add_document(d)

    classifier = Classifier()
    classifier.set_classifier(NaiveBayes())
    classifier.train_and_test(docs)
    classifier.output_probs()

    # clf = Classifier()
    #
    # for d in docs:
    #     driver.process_document(d)
    # print_features(docs[0])
    #
    # a = clf.train_and_test(docs, .3)
    # print a
    #
    #





# Utility functions
def print_features(doc):
    features = doc.get_features()
    separator = '%s\n' % ('#' * 12)
    result = separator + 'Features (%d):' % len(features) + '\n'  # TODO fix length
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


if __name__ == '__main__':
    main()



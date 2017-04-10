"""Driver for the classification package."""
from tokenizer import Tokenizer
from feature_extractor import FeatureExtractor
import utils
from corpus import Document
from classifier import Classifier
from naivebayes import NaiveBayes


class Processor:

    def __init__(self):
        """Set up tokenizer, feature extractor, and classifier"""
        self.tokenizer = Tokenizer(min_length=2)
        self.feature_ext = FeatureExtractor(min_freq=3)
        self.classifier = Classifier()

    def process_document(self, doc):
        """Tokenizes a new document and extracts its features."""
        if doc.raw_text is None:
            if doc.path:
                doc.raw_text = self.tokenizer.load_input(doc.path)
            # TODO else raise exception
        tokens = self.tokenizer.tokenize(doc.raw_text)
        features = self.feature_ext.process(tokens)
        doc.set_tokens(tokens)
        doc.set_features(features)

    def classify_document(self, doc):
        """Processes then classifies a new document."""
        if self.classifier.classifier is None:
            self.load_classifier('saved_classifier_4-7_7-60')
        self.process_document(doc)
        label = self.classifier.classify(doc)
        sublabel = self.classifier.subclassify(doc, label)
        return [label, sublabel]

    def load_classifier(self, path):
        """Loads a trained classifier from file.
        IMPORTANT: Doesn't load the associated corpus, so it can't train, just classify/test."""
        self.classifier.set_classifier(utils.load_object(path))

    def save_classifier(self, path):
        utils.save_object(self.classifier.classifier, path)


def build_doc_set(path):
    utils.batch_extract(path)
    path_list = utils.build_doc_set(path)
    docs = [Document(path=p, class_label=c, subclass_label=s) for p, c, s in path_list]
    # utils.print_docset(docs)
    return docs


def dev_train_test():
    """Train and test a new classifier on a directory of .txt documents."""
    docs = build_doc_set('../papers')
    # docs = build_doc_set(docs)
    driver = Processor()
    for d in docs:
        driver.process_document(d)
    driver.classifier.set_classifier(NaiveBayes())
    driver.classifier.train_and_test(docs, split=.1)


def dev_train():
    docs = build_doc_set('../papers')
    driver = Processor()
    for d in docs:
        driver.process_document(d)
    driver.classifier.set_classifier(NaiveBayes())
    driver.classifier.train(docs)
    utils.save_object(driver.classifier, 'saved_classifier-367')


def dev_test(test_doc):
    docs = build_doc_set('../papers')
    driver = Processor
    driver.process_document(test_doc)
    driver.classifier = utils.load_object('saved_classifier-367')
    driver.classifier.classify(test_doc)


def classify(text):
    driver = Processor()
    doc = Document(raw_text=text)
    driver.process_document(doc)
    driver.classifier = utils.load_object('saved_classifier-367')
    class_label = driver.classifier.classify(doc)
    subclass_label = driver.classifier.subclassify(doc, class_label)
    labels = [class_label, subclass_label]
    print labels
    return labels


def main():
    pass

if __name__ == '__main__':
    classifier = utils.load_object('saved_classifier-367')
    utils.print_corpus(classifier.corpus)
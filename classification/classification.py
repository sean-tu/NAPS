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
        self.clf = Classifier()

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
        if self.clf.classifier is None:
            self.load_classifier('saved_classifier-367-1')
        self.process_document(doc)
        utils.print_doc(doc)
        doc.class_label = doc.subclass_label = ''   # clear labels
        label = self.clf.classify(doc)
        sublabel = self.clf.subclassify(doc, label)
        doc.set_labels(label, sublabel)
        return [label, sublabel]

    def load_classifier(self, path):
        """Loads a trained classifier from file.
        IMPORTANT: Doesn't load the associated corpus, so it can't train, just classify/test."""
        main_clf = utils.load_object(path)
        sub_clfs = utils.load_object(path + '1')
        self.clf.set_classifier(main_clf)
        self.clf.subclassifiers = sub_clfs

    def save_classifier(self, path):
        """Saves Classifier.classifier to path and Classifier.subclassifiers to path1"""
        main_clf = self.clf.classifier
        sub_clfs = self.clf.subclassifiers
        utils.save_object(main_clf, path)
        utils.save_object(sub_clfs, path + '1')


def build_doc_set(path):
    utils.batch_extract(path)
    path_list = utils.build_doc_set(path)
    docs = [Document(path=p, class_label=c, subclass_label=s) for p, c, s in path_list]
    # utils.print_docset(docs)
    return docs


def dev_train_test():
    """Train and test a new classifier on a directory of .txt documents."""
    docs = build_doc_set('../papers')
    print 'Processing docset with %d docs...' % len(docs)
    driver = Processor()
    for d in docs:
        driver.process_document(d)
    driver.clf.set_classifier(NaiveBayes())
    driver.clf.train_and_test(docs, split=.07)


def dev_train():
    docs = build_doc_set('../papers')
    driver = Processor()
    for d in docs:
        driver.process_document(d)
    driver.clf.set_classifier(NaiveBayes())
    driver.clf.train(docs)
    driver.save_classifier('saved_classifier-367-1')


def dev_test():
    docs = build_doc_set('../papers')
    test_doc = docs[100]
    test_doc.class_label = test_doc.subclass_label = ''
    driver = Processor()
    labels = driver.classify_document(test_doc)
    print labels


def classify(text):
    driver = Processor()
    doc = Document(raw_text=text)
    driver.process_document(doc)
    driver.clf = utils.load_object('saved_classifier-367')
    class_label = driver.clf.classify(doc)
    subclass_label = driver.clf.subclassify(doc, class_label)
    labels = [class_label, subclass_label]
    print 'Labels: '
    print labels
    return labels


if __name__ == '__main__':
    dev_test()
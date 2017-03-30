import unittest
from classification import Processor
import cPickle as pickle
from corpus import Document
from classifier import Classifier



class TestClassification(unittest.TestCase):

    def setUp(self):
        self.driver = Processor()
        self.clf = Classifier()

    def test_classify_pickle(self):
        docs = load_file('docset.obj')
        print docs
        for d in docs:
            self.driver.process_document(d)
        print docs[0].get_features()
        accuracy = self.clf.train_and_test(docs, .1)
        print accuracy

    # def test_classify_movies(self):
    #
    #     """Classify movie reviews from nltk corpus"""
    #     from nltk.corpus import movie_reviews
    #     docs = [Document(raw_text=movie_reviews.raw(fileid), class_label=category)
    #             for category in movie_reviews.categories()
    #             for fileid in movie_reviews.fileids(category)]
    #
    #     #driver = Classification()
    #     for d in docs:
    #         self.driver.process_document(d)
    #
    #     print docs[1].get_features()
    #     #clf = Classifier()
    #     accuracy = self.clf.train_and_test(docs, .1) # train on 90%, test on 10% of document set
    #     self.assertGreater(accuracy, .7)        # must have at least 70% accuracy to pass


def load_file(path):
    with open(path, 'rb') as fin:
        return pickle.load(fin)


if __name__ == '__main__':
    unittest.main()
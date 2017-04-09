import random
import unittest
from corpus import *
from classifier import Classifier
from classification import Classification


class TestClassifier(unittest.TestCase):

    def test_classify_movies(self):
        """Classify movie reviews from nltk corpus"""
        from nltk.corpus import movie_reviews
        docs = [Document(raw_text=movie_reviews.raw(fileid), class_label=category)
                for category in movie_reviews.categories()
                for fileid in movie_reviews.fileids(category)]
        print docs


    def test_classify_China(self):
        # CHINA test from Standford Information Retrieval textbook
        chinatest = []
        doc1 = Document(raw_text="Chinese Beijing Chinese", class_label="China")
        doc2 = Document(raw_text="Chinese Chinese Shanghai", class_label="China")
        doc3 = Document(raw_text="Chinese Macao", class_label="China")
        doc4 = Document(raw_text="Tokyo Japan Japanese people are not Chinese", class_label="NotChina")
        doc5 = Document(raw_text="Chinese in China, Chinese Chinese, Tokyo in Japan")
        chinatest.append(doc1)
        chinatest.append(doc2)
        chinatest.append(doc3)
        chinatest.append(doc4)

        driver = Classification()
        for d in chinatest:
            driver.process_document(d)

        testcorp = Corpus()
        for d in chinatest:
            testcorp.add_doc(d)

        clf = Classifier()
        clf.set_classifier()
        clf.train(chinatest)

        driver.process_document(doc5)
        label = clf.classify(doc5)
        self.assertEquals('China', label)


if __name__ == '__main__':
    unittest.main()



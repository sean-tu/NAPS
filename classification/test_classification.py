import unittest
from corpus import *
from classification import *


class TestClassification(unittest.TestCase):

    def test_classify_movies(self):

        """Classify movie reviews from nltk corpus"""
        from nltk.corpus import movie_reviews
        docs = [Document(raw_text=movie_reviews.raw(fileid), class_label=category)
                for category in movie_reviews.categories()
                for fileid in movie_reviews.fileids(category)]

        driver = Classification()
        for d in docs:
            driver.process_document(d)

        print docs[1].get_features()
        clf = Classifier()
        accuracy = clf.train_and_test(docs, .1) # train on 90%, test on 10% of document set
        self.assertGreater(accuracy, .7)        # must have at least 70% accuracy to pass

if __name__ == '__main__':
    unittest.main()
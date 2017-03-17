"""
Implements the classification algorithm to assign a class label to a given document

In: feature set
Out: class label
"""

__author__ = 'Sean Reedy'


class Classifier:

    def __init__(self):
        self.classifier = None
        self.class_label = None

    def load_classifier(self, path):
        """Choose classifier to use for classification from file"""
        pass

    def set_classifier(self, path=None):
        self.classifier()

    def classify(self):
        pass
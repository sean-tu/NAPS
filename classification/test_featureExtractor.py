import unittest
from feature_extractor import FeatureExtractor

# Input: token list
tokens1 = ['test', 'file', 'cell', 'basic', 'unit', 'life', 'cellular', 'division', 'called', 'mitosis', 'living',
           'organisms', 'comprised', 'cells', 'microscopy', 'use', 'microscopes', 'see', 'objects', 'biologists',
           'study', 'biology', 'biologist', 'biological', 'entity', 'biologists', 'study', 'cool']

# Expected output from featurizing above
features1 = {'biology': 1, 'comprised': 1, 'microscopes': 1, 'see': 1, 'mitosis': 1, 'file': 1, 'biologist': 1, 'unit': 1, 'living': 1, 'use': 1, 'organisms': 1, 'cell': 1, 'basic': 1, 'test': 1, 'division': 1, 'life': 1, 'biologists': 2, 'objects': 1, 'cellular': 1, 'entity': 1, 'cool': 1, 'cells': 1, 'microscopy': 1, 'called': 1, 'biological': 1, 'study': 2}

test1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}


class TestFeatureExtractor(unittest.TestCase):

    def test_featurize1(self):
        f = FeatureExtractor()
        feats = f.featurize(tokens1)
        self.assertEquals(feats, features1)

    def test_stem_words(self):
        f = FeatureExtractor()
        s = f.stem_words({'connect':1, 'connected':1, 'connecting':1, 'connection':1})
        self.assertTrue(s == {'connect': 4})

    def test_filter_features(self):
        f = FeatureExtractor()
        filtered = f.filter_features(test1)
        print filtered
        self.assertTrue(filtered == {'c': 3, 'd': 4})


if __name__ == '__main__':
    unittest.main()
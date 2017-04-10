import unittest
from tokenizer import Tokenizer
import os

string1 = "Microscopy is the use of microscopes to see micro-sized objects."
str = ("This is a test file.\n"
       "\n"
       "The cell is the basic unit of life. Cellular division is\n"
       "called mitosis. All living organisms are comprised of cells.\n"
       "\n"
       "Microscopy is the use of microscopes to see micro-sized objects.\n"
       "\n"
       "Biologists study biology-- a biologist is a biological entity so biologists study themselves? Cool.")


class TestTokenizer(unittest.TestCase):

    def setUp(self):
        self.t = Tokenizer()

    def test_tokenize(self):
        tokens = self.t.tokenize(string1)
        self.assertEquals(tokens, ['microscopy', 'use', 'microscopes', 'see', 'objects', '.'])

    def test_tokenize_file(self):
        t = Tokenizer()
        cwd = os.getcwd()
        print os.listdir(cwd)
        raw = t.load_input(path='classification/paper1.txt')
        tokens = t.tokenize(raw)
        self.assertGreater(len(tokens), 3000)   # Check a reasonable number of tokens were successfully extracted

    def test_filter_tokens(self):
        t = Tokenizer()
        tokens = t.tokenize(string1)
        filtered = t.filter_tokens(tokens)
        self.assertEquals(filtered,
                          ['microscopy', 'use', 'microscopes', 'see','objects'])

    def test_tokenizer_long(self):
        t = Tokenizer()
        tokens = t.tokenize(str)
        filtered = t.filter_tokens(tokens)
        print filtered


if __name__ == '__main__':
    unittest.main()
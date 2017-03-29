import unittest
from tokenizer import Tokenizer

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

    def test_tokenize(self):
        t = Tokenizer()
        tokens = t.tokenize(string1)
        self.assertEquals(tokens, ['Microscopy', 'is', 'the', 'use', 'of', 'microscopes', 'to', 'see', 'micro-sized', 'objects', '.'])

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
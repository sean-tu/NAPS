import unittest
from tokenizer import Tokenizer

string1 = "Microscopy is the use of microscopes to see micro-sized objects."


class TestTokenizer(unittest.TestCase):

    def test_tokenize(self):
        t = Tokenizer(text=string1)
        t.tokenize()
        self.assertEquals(t.tokens, ['Microscopy', 'is', 'the', 'use', 'of', 'microscopes', 'to', 'see', 'micro-sized', 'objects', '.'])

    def test_filter_tokens(self):
        t = Tokenizer(text=string1)
        t.tokenize()
        t.filter_tokens()
        self.assertEquals(t.tokens,
                          ['microscopy', 'use', 'microscopes', 'see','objects'])


if __name__ == '__main__':
    unittest.main()
# -*- coding: UTF-8 -*-

import platform

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest

import os
import tempfile
from trigrams import TrigramsDB

class TestGeneration(unittest.TestCase):

    def setUp(self):
        self.path = tempfile.NamedTemporaryFile(delete=False).name
        self.tb = TrigramsDB()

    def tearDown(self):
        os.unlink(self.path)

    def setContent(self, content):
        with open(self.path, 'w') as f:
            f.write(content)

    def getContent(self):
        with open(self.path, 'r') as f:
            return f.read()

    # feed

    def test_feed_none(self):
        self.tb.feed()
        self.assertEquals({}, self.tb._db)

    def test_feed_text_less_than_three_words(self):
        self.tb.feed('Hello world!')
        self.assertEquals({}, self.tb._db)

    def test_feed_text(self):
        self.tb.feed('Hello, my name is Foo.')
        self.assertEquals({
            'hello,###my' : ['name'],
            'my###name' : ['is'],
            'name###is': ['Foo.']
        }, self.tb._db)

    def test_feed_text_repetitions(self):
        self.tb.feed('This is the man who is the dog')
        self.assertEquals({
            'this###is': ['the'],
            'is###the': ['man', 'dog'],
            'the###man': ['who'],
            'man###who': ['is'],
            'who###is': ['the'],
        }, self.tb._db)

    def test_feed_from_file(self):
        self.setContent('a b c')
        self.tb.feed(source=self.path)
        self.assertEquals({'a###b':['c']}, self.tb._db)

    def test_feed_from_text_and_file(self):
        self.setContent('a b c')
        self.tb.feed('a b d', source=self.path)
        self.assertEquals({'a###b':['d', 'c']}, self.tb._db)

    # generate

    def test_generate_empty_db(self):
        self.assertEquals('', self.tb.generate())

    def test_generate_max_words(self):
        txt = 'foo bar qux'
        self.assertEquals(txt, self.tb.generate(words=txt.split(' '), wlen=3))

    def test_generate_from_one_word(self):
        self.tb._db = {'a###b':['c']}
        self.assertEquals('a b c', self.tb.generate(words=['a'], wlen=3))

    def test_generate_from_no_word(self):
        self.tb._db = {'a###b':['c']}
        self.assertEquals('a b c', self.tb.generate(wlen=3))

    def test_generate_with_no_more_words(self):
        self.tb._db = {'a###b':['c']}
        self.assertEquals('a b c', self.tb.generate(wlen=1000))

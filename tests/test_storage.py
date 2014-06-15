# -*- coding: UTF-8 -*-

import platform

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest

import os
import json
import tempfile
from trigrams import TrigramsDB

class TestDBStorage(unittest.TestCase):

    def setUp(self):
        self.path = tempfile.NamedTemporaryFile(delete=False).name
        self.tb = TrigramsDB()

    def tearDown(self):
        os.unlink(self.path)

    def setContent(self, content):
        with open(self.path, 'w') as f:
            f.write(json.dumps(content))

    def getContent(self):
        with open(self.path, 'r') as f:
            return json.loads(f.read())

    # init

    def test_init_with_no_file(self):
        self.assertEquals({}, self.tb._db)

    def test_init_with_file(self):
        db = {'foo': 'bar'}
        self.setContent(db)
        tb = TrigramsDB(self.path)
        self.assertEquals(db, tb._db)

    # save

    def test_save_with_no_file(self):
        self.tb.save()

    def test_save_empty_db_with_output(self):
        self.tb.save(self.path)
        self.assertEquals({}, self.getContent())

    def test_save_empty_db_with_dbfile(self):
        self.tb.dbfile = self.path
        self.tb.save()
        self.assertEquals({}, self.getContent())

    def test_db(self):
        db = {'foo': 'bar', 'qux': [1,2,3]}
        self.tb._db = db
        self.tb.dbfile = self.path
        self.tb.save()
        self.assertEquals(db, self.getContent())

    # _dump

    def test_dump(self):
        db = {'foo':'bar', 42:3, '17': '@'}
        self.tb._db = db
        self.assertEquals(json.dumps(db), self.tb._dump())

    # _load

    def test_load(self):
        db = {'bar': 42}
        self.setContent(db)
        self.tb.dbfile = self.path
        self.tb._load()
        self.assertEquals(db, self.tb._db)

    # _sanitize

    def test_sanitize_empty(self):
        self.assertEquals('', self.tb._sanitize(''))

    def test_sanitize_word(self):
        w = 'foo'
        self.assertEquals(w, self.tb._sanitize(w))

    def test_sanitize_word_special_chars(self):
        w = 'Foo.'
        self.assertEquals(w, self.tb._sanitize(w))

    def test_sanitize_word_with_sep(self):
        w = 'Foo' + TrigramsDB._WSEP + 'bar'
        self.assertEquals('Foobar', self.tb._sanitize(w))

    # _insert

    def test_insert_trigram_empty_db(self):
        words = ['Foo', 'bar,', 'qux']
        self.tb._insert(words)
        self.assertEquals({'foo###bar,':['qux']}, self.tb._db)

    def test_insert_trigram_already_here(self):
        words = ['Foo', 'bar,', 'qux']
        self.tb._insert(words)
        self.tb._insert(words)
        self.assertEquals({'foo###bar,':['qux']}, self.tb._db)

    def test_insert_trigram_already_here_different_case(self):
        words = ['Foo', 'bar,', 'qux']
        self.tb._insert(words)
        self.tb._insert(['foo', 'Bar,', 'qux'])
        self.assertEquals({'foo###bar,':['qux']}, self.tb._db)

    def test_insert_trigram_already_here_different_case_last_word(self):
        words = ['Foo', 'bar,', 'qux']
        self.tb._insert(words)
        self.tb._insert(['foo', 'Bar,', 'Qux'])
        self.assertEquals({'foo###bar,':['qux', 'Qux']}, self.tb._db)

    def test_insert_trigram(self):
        self.tb._insert(['a', 'b', 'c'])
        self.tb._insert(['a', 'b', 'd'])
        self.tb._insert(['A', 'b', 'e'])
        self.tb._insert(['x', 'y###', 'z'])
        self.assertEquals({'a###b':['c', 'd', 'e'], 'x###y':['z']},
                          self.tb._db)

    # _get

    def test_get_empty_db(self):
        self.assertIs(None, self.tb._get('a', 'b'))

    def test_get_impossible(self):
        self.tb._db = {'a###b': ['c']}
        self.assertIs(None, self.tb._get('a', 'c'))

    def test_get_one_possib(self):
        self.tb._db = {'a###b': ['c']}
        self.assertEquals('c', self.tb._get('a', 'b'))

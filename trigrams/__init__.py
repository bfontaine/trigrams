# -*- coding: UTF-8 -*-

"""
Simple trigrams-based text generation
"""

__version__ = '0.1.0'

import re
import json
from random import sample


class TrigramsDB(object):
    """
    A trigrams database. It has two main methods: ``feed``, to initialize it
    with some existing text, and ``generate``, to generate some new text. The
    more text you feed it, the more "random" the generated text will be.
    """

    _WSEP = '###'  # words separator

    def __init__(self, dbfile=None):
        """
        Initialize a new trigrams database. If ``dbfile`` is given, the
        database is read and written from/to this file.
        """
        self.dbfile = dbfile
        self._load()

    def save(self, output=None):
        """
        Save the database to a file. If ``output`` is not given, the ``dbfile``
        given in the constructor is used.
        """
        if output is None:
            if dbfile is None:
                return
            output = self.dbfile

        with open(output, 'w') as f:
            f.write(self._dump())

    def feed(self, text=None, source=None):
        """
        Feed some text to the database, either from a string (``text``) or a
        file (``source``).

        >>> db = TrigramsDB()
        >>> db.feed("This is my text")
        >>> db.feed(source="some/file.txt")
        """
        if text is not None:
            words = re.split(r'\s+', text)
            wlen = len(words)
            for i in range(wlen - 2):
                self._insert(words[i:i+3])

        if source is not None:
            with open(source, 'r') as f:
                self.feed(f.read())

    def generate(self, **kwargs):
        """
        Generate some text from the database. By default only 70 words are
        generated, but you can change this using keyword arguments.

        Keyword arguments:

            - ``wlen``: maximum length (words)
            - ``words``: a list of words to use to begin the text with
        """
        words = list(map(self._sanitize, kwargs.get('words', [])))
        max_wlen = kwargs.get('wlen', 70)

        wlen = len(words)

        if wlen < 2:
            if not self._db:
                return ''

            if wlen == 0:
                words = sample(self._db.keys(), 1)[0].split(self._WSEP)
            elif wlen == 1:
                spl = [k for k in self._db.keys()
                       if k.startswith(words[0]+self._WSEP)]
                words.append(sample(spl, 1)[0].split(self._WSEP)[1])

            wlen = 2

        while wlen < max_wlen:
            next_word = self._get(words[-2], words[-1])
            if next_word is None:
                break

            words.append(next_word)
            wlen += 1

        return ' '.join(words)

    def _load(self):
        """
        Load the database from its ``dbfile`` if it has one
        """
        if self.dbfile is not None:
            with open(self.dbfile, 'r'):
                self._db = json.loads(f.read())
        else:
            self._db = {}

    def _dump(self):
        """
        Return a string version of the database, which can then be used by
        ``_load`` to get the original object back.
        """
        return json.dumps(self._db)

    def _get(self, word1, word2):
        """
        Return a possible next word after ``word1`` and ``word2``, or ``None``
        if there's no possibility.
        """
        key = self._WSEP.join([self._sanitize(word1), self._sanitize(word2)])
        key = key.lower()
        if key not in self._db:
            return

        return sample(self._db[key], 1)[0]

    def _sanitize(self, word):
        """
        Sanitize a word for insertion in the DB
        """
        return word.replace(self._WSEP, '')

    def _insert(self, trigram):
        """
        Insert a trigram in the DB
        """
        words = list(map(self._sanitize, trigram))

        key = self._WSEP.join(words[:2]).lower()
        next_word = words[2]

        self._db.setdefault(key, [])
        # we could use a set here, but sets are not serializables in JSON. This
        # is the same reason we use dicts instead of defaultdicts.
        if next_word not in self._db[key]:
            self._db[key].append(next_word)

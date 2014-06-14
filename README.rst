========
trigrams
========

.. image:: https://img.shields.io/travis/bfontaine/trigrams.png
   :target: https://travis-ci.org/bfontaine/trigrams
   :alt: Build status

.. image:: https://coveralls.io/repos/bfontaine/trigrams/badge.png?branch=master
   :target: https://coveralls.io/r/bfontaine/trigrams?branch=master
   :alt: Coverage status

.. image:: https://img.shields.io/pypi/v/trigrams.png
   :target: https://pypi.python.org/pypi/trigrams
   :alt: Pypi package

.. image:: https://img.shields.io/pypi/dm/trigrams.png
   :target: https://pypi.python.org/pypi/trigrams

``trigrams`` is a simple trigrams-based random text generation Python module.

Install
-------

.. code-block::

    [sudo] pip install trigrams

The library works with both Python 2.x and 3.x.

Usage
-----

`Read the docs`_. ::

    from trigrams import TrigramsDB
    db = TrigramsDB()
    db.feed("My interesting text")
    for f in ['source1.txt', 'source2.txt', 'source3.txt']:
        db.feed(source=f)

    print db.generate()


.. _Read the docs: http://trigrams.readthedocs.org/en/latest/api_reference.html

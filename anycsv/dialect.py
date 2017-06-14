#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from anycsv import csv

POSSIBLE_DELIMITERS = [',', '\t', ';', '#', ':', '|', '^']


def guessDialect(file_content):
    dialect = csv.Sniffer().sniff(file_content, POSSIBLE_DELIMITERS)

    if dialect is None:
        raise Exception('cannot guess dialect')

    return {
        'delimiter': dialect.delimiter,
        'doublequote': dialect.doublequote,
        'lineterminator': dialect.lineterminator,
        'quotechar': dialect.quotechar,
        'quoting': dialect.quoting,
        'skipinitialspace': dialect.skipinitialspace
    }

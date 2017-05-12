#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
class Table():
    def __init__(self, filename=None, url=None):
        self.filename = filename
        self.url=url
        self.csvReader = None
        self.delimiter = None
        self.quotechar = '"'
        self.encoding = None
        self.columns = -1
        self.dialect = None

    def __iter__(self):
        return self

    def next(self):
        return self.csvReader.next()

    def seek_line(self, line_number):
        self.csvReader.seek_line(line_number)

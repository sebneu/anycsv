#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

class AnyCSVException(Exception):
    pass


class NoDelimiterException(AnyCSVException):
    pass

class FileSizeException(Exception):
    pass
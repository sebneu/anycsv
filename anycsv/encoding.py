#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
__author__ = 'jumbrich'

import subprocess
#import chardet
#from chardet.universaldetector import UniversalDetector
from cchardet import UniversalDetector
import magic

#from chardet.chardetect import UniversalDetector
#import bs4

# UnicodeDammit was refactored a lot recently.
# It now falls back on cchardet if its in the path.
# Otherwise, we have to make sure that it does *not* fall back on
# chardet as it is slow and has only minimal charset coverage.
#if not 'cchardet' in bs4.dammit.__dict__:
#    # Either chardet or nothing
#    bs4.dammit.chardet_dammit = lambda string: None


def get_header_encoding(header):
    cont_type = None
    if 'Content-Type' in header:
        cont_type = header['Content-Type']
    elif 'content-type' in header:
        cont_type = header['content-type']

    header_encoding = None
    if cont_type and len(cont_type.split(';')) > 1:
        header_encoding = cont_type.split(';')[1]
        header_encoding = header_encoding.strip()
        if 'charset=' in header_encoding:
            header_encoding = header_encoding[8:]
        elif 'charset = ' in header_encoding:
            header_encoding = header_encoding[10:]
        elif 'charset =' in header_encoding:
            header_encoding = header_encoding[9:]
    return header_encoding

def get_charset(filename):
    ''' returns the charset of a file using the unix tool 'file' '''
    output = None
    try:
        proc = subprocess.Popen('file -bi %s' % filename,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                )
        output = proc.stdout.readline()
        output = output.split('=')[1].strip()
    except Exception:
        return None
    return output

def guessEncoding(content, header=None):
    results = {'default': {'encoding': 'utf8'}}
    results['lib_chardet'] = guessWithChardet(content)
    results['magic']= guessWithMagic(content)

    if header:
        header_encoding = get_header_encoding(header)
        results['header'] = {'encoding': header_encoding}

    return results


def guessWithChardet(content):
    u = UniversalDetector()
    for line in content.split(b"\n"):
        u.feed(line)
    u.close()
    result = u.result
    return result


def guessWithMagic(content):
    if hasattr(magic, 'detect_from_content'):
        # support for "file-magic" library
        result = magic.detect_from_content(content)
        result = result.__dict__
    else:
        # support for "filemagic" library (mac-os)
        with magic.Magic(flags=magic.MAGIC_MIME_ENCODING) as m:
            e = m.id_buffer(content)
        result = {'encoding': e}
    return result


# #worth to look into
# #https://bitbucket.org/Telofy/utilofies/csvprofiler/0d8cdc3ae5a0a08e7fb5906d96f0d8e2284751d1/utilofies/bslib.py?at=master#cl-15
# def intelligent_decode(fname):
#     """ One problem remains in the latest version of UnicodeDammit, namely
#         that pages that have beautifully declared encodings but contain one
#         small erroneous byte sequence somewhere will fail to be decoded with
#         the mostly correct encodings, while Windows-1252 somehow succeeds, but
#         completely mucks up all umlauts and ligatures. Hence I want to remove
#         Windows-1252 from the potential encodings.
#
#         I don't fall back on cchardet just yet.
#     """
#     detector = bs4.dammit.EncodingDetector(fname)
#     # Fall back on forcing it to UTF-8 only if no other encodings
#     # could be found. (I use override_encodings for the HTTP encoding,
#     # which seems at least less reliable to me than the declared encoding.)
#     potential_encodings = \
#         filter(bool, [detector.sniffed_encoding, detector.declared_encoding]
#                + list(detector.override_encodings)) \
#         or ['utf-8']
#     contains_replacement_characters = False
#     tried_encodings = []
#     unicode_markup = None
#     original_encoding = None
#     for encoding in potential_encodings:
#         tried_encodings.append(encoding)
#         try:
#             unicode_markup = detector.markup.decode(encoding)
#         except Exception as excp:
#             #logger.info('Unsuccessfully tried encoding %s: %r', encoding, excp)
#             print 'Unsuccessfully tried encoding %s: %r', encoding, excp
#         if unicode_markup is not None:
#             original_encoding = encoding
#             break
#     if unicode_markup is None:
#         # Whatever!
#         unicode_markup = detector.markup.decode(
#             potential_encodings[0], 'replace')
#         original_encoding = potential_encodings[0]
#         contains_replacement_characters = True
#     return type(b'MockDammit', (object,), {
#         'contains_replacement_characters': contains_replacement_characters,
#         'original_encoding': original_encoding,
#         'detector': detector,
#         'is_html': detector.is_html,
#         'markup': detector.markup,
#         'tried_encodings': tried_encodings,
#         'unicode_markup': unicode_markup})
import os
import csv
import logging
import StringIO
import requests
import dialect
import encoding
from parser.csv_model import Table
from tools import io

DEFAULT_ENCODING='utf-8'

class CSVParser():
    enc_priority=['lib_chardet', 'header', 'default']


    @classmethod
    def get_table(cls, fName=None, url=None, content=None):
        logger = logging.getLogger(__name__)

        if not fName and not url and not content:
            raise IOError('No CSV input specified')

        meta = CSVParser.sniff_metadata(fName, url, content)
        table = Table(url=url, fName=fName)

        dialect = meta['dialect']
        if 'delimiter' in dialect:
            table.delimiter = dialect['delimiter']
        if 'quotechar' in dialect:
            table.quotechar = dialect['quotechar']

        table.encoding = meta['used_enc']

        if content:
            input = StringIO.StringIO(content)
        elif fName and os.path.exists(fName):
            input = open(fName, 'rU')
        elif url:
            input = requests.get(url, stream=True).iter_lines()
        else:
            raise IOError('No CSV input specified')

        if table.encoding and ('utf-8' in table.encoding or 'utf8' in table.encoding):
            table.csvReader = UnicodeReader(input,
                                            delimiter=table.delimiter,
                                            quotechar=table.quotechar)
        else:
            table.csvReader = EncodedCsvReader(input,
                                         encoding=table.encoding,
                                         delimiter=table.delimiter,
                                         quotechar=table.quotechar)

        table.headers = table.csvReader.next()
        table.numCols = len(table.headers)
        return table


    @classmethod
    def sniff_metadata(cls, fName= None, url=None, content=None, header=None, sniffLines=100):
        logger = logging.getLogger(__name__)
        id = url if url is not None else fName

        if not any([fName,url]) and not any([content, header]):
            #we need at least one of the three, so return empty results
            return {}

        if not any([content, header]) and any([fName, url]):
            res = io.getContentAndHeader(fName=fName, url=url, download_dir="/tmp/", max_lines=sniffLines)
            content, header = res['content'], res['header']

        logger.debug('(%s) Extracting CSV meta data ', id)
        meta = cls.extract_csv_meta(header=header, content=content)
        logger.debug("(%s) Meta %s ", id, meta)

        return meta

    @classmethod
    def extract_csv_meta(cls, header, fName=None, content=None, id=''):
        logger = logging.getLogger(__name__)

        results = {'used_enc':None,
                   'enc': encoding.guessEncoding(content, header),
                   'dialect':{}}

        content_encoded = None
        status="META "
        c_enc = None
        for k in cls.enc_priority:
            #we try to use the different encodings
            try:
                if k in results['enc'] and results['enc'][k]['encoding'] is not None:
                    content_encoded = content.decode(encoding=results['enc'][k]['encoding'])
                    c_enc = results['enc'][k]['encoding']
                    status+=" encoding"
                    break
            except Exception as e:
                logger.debug('(%s) ERROR Tried %s encoding: %s', results['enc'][k]['encoding'],id, e)
        if content_encoded:
            results['used_enc'] = c_enc
            try:
                results['dialect'] = dialect.guessDialect(content_encoded)
                status+=" dialect"
            except Exception as e:
                logger.warning('(%s)  %s',id, e.message)
                results['dialect']={}
        else:
            try:
                results['dialect'] = dialect.guessDialect(content)
                status+=" dialect"
            except Exception as e:
                logger.warning('(%s) Cannot guess the dialect: %s',id, e.message)
                results['dialect']={}

        if fName:
            results['charset'] = encoding.get_charset(fName)

        logger.info("(%s) %s", id,status)
        return results


class EncodedCsvReader:
    def __init__(self, f, encoding="utf-8-sig", delimiter="\t", quotechar="'",  eol="\n", **kwds):
        self.encoding=encoding
        if not quotechar:
            quotechar="'"
        if not encoding:
            self.encoding='utf-8-sig'

        if not delimiter:
            self.reader = csv.reader(f, quotechar=quotechar.encode('ascii'), **kwds)
        else:
            self.reader = csv.reader(f, delimiter=delimiter.encode('ascii'), quotechar=quotechar.encode('ascii'), **kwds)

    def next(self):
        row = self.reader.next()
        result = [unicode(s.decode(self.encoding)) for s in row]
        return result

    def __iter__(self):
        return self


class UnicodeReader(object):
    def __init__(self, f, delimiter="\t", quotechar="'", encoding='utf-8', errors='strict',
                 **kwds):
        format_params = ['delimiter', 'doublequote', 'escapechar', 'lineterminator', 'quotechar', 'quoting', 'skipinitialspace']
        #if dialect is None:
        #    if not any([kwd_name in format_params for kwd_name in kwds.keys()]):
        #        dialect = csv.excel
        if not quotechar:
            quotechar="'"
        if not encoding:
            encoding='utf-8'
        if not delimiter:
            self.reader = csv.reader(f, quotechar=quotechar.encode('ascii'), **kwds)
        else:
            self.reader = csv.reader(f, delimiter=delimiter.encode('ascii'), quotechar=quotechar.encode('ascii'), **kwds)
        self.encoding = encoding
        self.encoding_errors = errors

    def next(self):
        row = self.reader.next()
        encoding = self.encoding
        encoding_errors = self.encoding_errors
        float_ = float
        unicode_ = unicode
        return [(value if isinstance(value, float_) else
                 unicode_(value, encoding, encoding_errors)) for value in row]

    def __iter__(self):
        return self

    @property
    def dialect(self):
        return self.reader.dialect

    @property
    def line_num(self):
        return self.reader.line_num

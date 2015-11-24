__author__ = 'jumbrich'


import csv

#removed stupid " "
POSSIBLE_DELIMITERS = [',', '\t', ';', '#', ':', '|','^']

def sniff_dialect(sample):
    """
    A functional version of ``csv.Sniffer().sniff``, that extends the
    list of possible delimiters to include some seen in the wild.
    """
    try:
        dialect = csv.Sniffer().sniff(sample, POSSIBLE_DELIMITERS)
    except:
        dialect = None

    return dialect

def guessDialect(file_content):

    return guessDialectWithLibCSV(file_content)


def guessDialectWithLibCSV(file_content):
    """

    :param file_content: the file content of the csv file
    :return: a csv dialect object
    """
    dialect = sniff_dialect(file_content)

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

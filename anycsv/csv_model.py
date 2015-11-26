class Table():
    def __init__(self, filename=None, url=None):
        self.filename = filename
        self.url=url
        self.csvReader = None
        self.delimiter = None
        self.quotechar = '"'
        self.encoding = None
        self.columns = -1

    def __iter__(self):
        return self

    def next(self):
        return self.csvReader.next()

    def seek(self, offset, whence=0):
        self.csvReader.seek(offset, whence)

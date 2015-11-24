class Table():
    def __init__(self, fName=None, url=None):
        self.headers = []
        self.description = []
        self.fName= fName
        self.url=url
        self.csvReader = None
        self.delimiter = None
        self.quotechar = '"'
        self.encoding = None
        self.numCols = -1

    def add_description(self, descr):
        self.description.append(descr)

    def __iter__(self):
        return self

    def next(self):
        return self.csvReader.next()

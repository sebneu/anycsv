from collections import defaultdict
import time

from parser.csv_parser import CSVParser
import os

__author__ = 'sebastian'



if __name__ == '__main__':
    root = "tmp/data_gv_at/"
    times = []
    delimiter = defaultdict(int)
    width = defaultdict(int)
    encoding = defaultdict(int)
    for file in os.listdir(root):
        if file.endswith(".csv"):
            try:
                start = time.clock()
                table = CSVParser.get_table(fName=os.path.join(root, file))
                for i, row in enumerate(table):
                    if i > 100:
                        break
                end = time.clock()
                print end-start
                times.append(end - start)
                delimiter[table.delimiter] += 1
                width[table.numCols] += 1
                encoding[table.encoding] += 1
            except Exception as e:
                print 'File', file
                print e

    avg_time = sum(times) / float(len(times))

    print 'avg_time', avg_time
    print 'delimiter', delimiter
    print 'width', width
    print 'encoding', encoding
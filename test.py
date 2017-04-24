import anycsv
import csv

# filename = 'path/to/file.csv'
# reader = anycsv.reader(filename=filename)

# url = 'http://file.csv'
# reader = anycsv.reader(url=url)

content = 'a,b,c\n1,2,3\n4,5,6'
reader = anycsv.reader(content=content)

with open('testfile.csv', 'w') as f:
    writer = csv.writer(f, delimiter='|')
    writer.writerows([row for row in reader])

import sys
import csv

with open('E://User/work_python/sc/data/ownthink_v2/ownthink_v2.csv', 'r', encoding='utf8') as fin:
    reader = csv.reader(fin)
    for index, read in enumerate(reader):
        print(read)

        if index > 10000000:
            sys.exit(0)
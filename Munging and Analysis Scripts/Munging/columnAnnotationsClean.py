'''
Created on May 15, 2013

@author: Bhushan Ramnani (bramnani@cs.cmu.edu)
Python script to restructure the column_annotations file of the keystroke data.
Add a new column called category and assign value to it based on the annotated row category
'''

import csv
import sys

def main():
    fileToOpen = open(sys.argv[1])
    fnameTowrite = sys.argv[1]
    fnameTowrite = fnameTowrite.replace(".csv", "")
    fnameTowrite = fnameTowrite+'Clean.csv'
    fileToWrite = open(fnameTowrite,"wb")
    reader = csv.reader(fileToOpen)
    writer = csv.writer(fileToWrite)
    x = 0;
    labels = []

    for row in reader:
        category = ""
        if x==0:
            x=1
            labels = row
            header = labels[0:4]
            header.append("Categories")
            writer.writerow(header)
            continue
        for i in xrange(4, len(row)):
            if row[i]=='1':
                if category == '':
                    category = labels[i]
                else:
                    category = category+','+labels[i]
        row = row[0:4]#
        row.append(category)
        writer.writerow(row)


main()

if __name__ == '__main__':
    pass
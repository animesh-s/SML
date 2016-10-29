import csv
import os
from create_csv import build_csv

if __name__ == "__main__":
    values = []
    with open('../../../../dataset/edits.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            comment = row['editcomment']
            if comment == 'null':
                comment = ''
            values.append(len(comment))
    build_csv(values)
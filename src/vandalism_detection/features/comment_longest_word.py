import csv
import os
from create_csv import initialize, build_csv

if __name__ == "__main__":
    values, T = initialize()
    with open('../../../../dataset/edits.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            comment = row['editcomment']
            if comment == 'null':
                comment = ''
            max_length = 0
            words = comment.split()
            for word in words:
                max_length = max(max_length, len(word))
            values.append(max_length)
            T = T - 1
            if T == 0:
                break
    build_csv(values)

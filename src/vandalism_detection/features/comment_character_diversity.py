import csv
import os
from create_csv import initialize, build_csv
from character_diversity import get_unique_char_count

if __name__ == "__main__":
    values, T = initialize()
    with open('../../../../dataset/edits.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            comment = row['editcomment']
            if comment == 'null':
                comment = ''
            if not comment:
                diversity = 0
            else:
                unique_char_count = get_unique_char_count(comment)
                if unique_char_count == 0:
                    diversity = 0
                else:
                    diversity = round(pow(len(comment),1.0/unique_char_count), 2)
            values.append(diversity)
            T = T - 1
            if T == 0:
                break
    build_csv(values)
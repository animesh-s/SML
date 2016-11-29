import csv
import os
from create_csv import initialize, build_csv
from character_distribution import get_prob_dist, get_entropy

if __name__ == "__main__":
    values, T = initialize()
    with open('../../../../dataset/edits.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            comment = row['editcomment']
            if comment == 'null':
                comment = ''
            if not comment:
                entropy = 0
            else:
                prob_dist = get_prob_dist(comment)
                entropy = get_entropy(prob_dist)
            values.append(entropy)
            T = T - 1
            if T == 0:
                break
    build_csv(values)
import csv
import os
from create_csv import initialize, build_csv
from word_categories import calculate_vulgarism_ratio, calculate_biased_ratio, calculate_pronoun_ratio, calculate_word_categories_ratios

if __name__ == "__main__":
    values, T = initialize()
    with open('../../../../dataset/edits.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            comment = row['editcomment']
            if comment == 'null':
                comment = ''
            ratios = calculate_word_categories_ratios(comment.split())
            values.append(ratios)
            T = T - 1
            if T == 0:
                break
    build_csv(values)
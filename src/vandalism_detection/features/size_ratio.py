import csv
from search_file import find
from create_csv import initialize, build_csv

def calculate_ratio(old_size, new_size):
    return ((float)(1 + old_size) / (1 + new_size))

if __name__ == "__main__":
    values, T = initialize()
    with open('../../../../dataset/edits.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            oldrevisionid = row['oldrevisionid']
            newrevisionid = row['newrevisionid']
            old_revision_path = find(oldrevisionid+'.txt', '../../../../dataset/article-revisions/')
            new_revision_path = find(newrevisionid+'.txt', '../../../../dataset/article-revisions/')
            old_text = open(old_revision_path,'r').read()
            new_text = open(new_revision_path,'r').read()
            ratio = calculate_ratio(len(old_text), len(new_text))
            values.append(ratio)
            T = T - 1
            if T == 0:
                break
    build_csv(values)
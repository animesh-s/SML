import re
import csv
from search_file import find
from create_csv import initialize, build_csv
from diff_match_patch import diff_match_patch

def calculate_ratio(digit_count, total_count):
    return ((1.0 + digit_count) / (1.0 + total_count))

if __name__ == "__main__":
    values, T = initialize()
    diff_object = diff_match_patch()
    with open('../../../../dataset/edits.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            oldrevisionid = row['oldrevisionid']
            newrevisionid = row['newrevisionid']
            old_revision_path = find(oldrevisionid+'.txt', '../../../../dataset/article-revisions/')
            new_revision_path = find(newrevisionid+'.txt', '../../../../dataset/article-revisions/')
            old_text = open(old_revision_path,'r').read()
            new_text = open(new_revision_path,'r').read()
            diff = diff_object.diff_main(old_text, new_text)
            additions = [item[1] for item in diff if item[0] == 1]
            inserted_text = "".join(additions)
            inserted_text = inserted_text.replace(" ", "")
            digits = "".join(re.findall('\d+', inserted_text))
            ratio = calculate_ratio(len(digits), len(inserted_text))
            values.append(ratio)
            T = T - 1
            if T == 0:
                break
    build_csv(values)
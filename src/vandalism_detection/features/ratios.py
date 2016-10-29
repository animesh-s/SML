import re
import csv
from search_file import find
from create_csv import initialize, build_csv
from diff_match_patch import diff_match_patch
from edit import diff_inserted_text

def calculate_size_ratio(old_size, new_size):
    return ((1.0 + old_size) / (1.0 + new_size))

def calculate_digit_ratio(digit_count, total_count):
    return ((1.0 + digit_count) / (1.0 + total_count))

def calculate_upper_to_lower_case_ratio(upper_count, lower_count):
    return ((1.0 + upper_count) / (1.0 + lower_count))

def calculate_upper_to_all_ratio(upper_count, lower_count):
    return ((1.0 + upper_count) / (1.0 + lower_count + upper_count))

def calculate_non_alphanumeric_ratio(non_alphanumeric_count, total_count):
    return ((1.0 + non_alphanumeric_count) / (1.0 + total_count))

def calculate_ratios(old_text, new_text):
    size_ratio = calculate_size_ratio(len(old_text), len(new_text))
    inserted_text = diff_inserted_text(old_text, new_text)
    digits = "".join(re.findall('\d+', inserted_text))
    total_count = len(inserted_text)
    digit_ratio = calculate_digit_ratio(len(digits), total_count)
    upper_count = len(re.findall(r'[A-Z]', inserted_text))
    lower_count = len(re.findall(r'[a-z]', inserted_text))
    upper_to_lower_ratio = calculate_upper_to_lower_case_ratio(upper_count, lower_count)
    upper_to_all_ratio = calculate_upper_to_all_ratio(upper_count, lower_count)
    non_alphanumeric_count = len(re.findall(r'\W', inserted_text))
    non_alphanumeric_ratio = calculate_non_alphanumeric_ratio(non_alphanumeric_count, total_count)
    ratios = str(size_ratio) + ',' + str(digit_ratio) + ',' + str(upper_to_lower_ratio) + ',' + str(upper_to_all_ratio) + ',' + str(non_alphanumeric_ratio)
    return ratios

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
            ratios = calculate_ratios(old_text, new_text)
            values.append(ratios)
            T = T - 1
            if T == 0:
                break
        build_csv(values)
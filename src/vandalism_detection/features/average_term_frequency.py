import re
import csv
from search_file import find
from edit import diff_inserted_words
from create_csv import initialize, build_csv

def calculate_average_term_frequency(inserted_words, new_text_words):
    inserted_dict = {}
    new_text_dict = {}
    frequency_inserted_dict = {}
    frequency_new_text_dict = {}
    value = 0
    total_inserted_words = len(inserted_words)
    total_new_text_words = len(new_text_words)
    average_term_frequency = 0
    for word in inserted_words:
        if word in inserted_dict:
            inserted_dict[word] = inserted_dict[word] + 1
        else:
            inserted_dict[word] = 1
    for word in inserted_dict:
       if word not in frequency_inserted_dict:
            frequency_inserted_dict[word] = (float)(inserted_dict[word]) / total_inserted_words
    for word in new_text_words:
        if word in inserted_dict:           
            if word in new_text_dict:
                new_text_dict[word] = new_text_dict[word] + 1
            else:
                new_text_dict[word] = 1
    for word in new_text_dict:
        if word not in frequency_new_text_dict:
            frequency_new_text_dict[word] = (float)(new_text_dict[word]) / total_new_text_words
    for word in inserted_dict:
        if word in frequency_new_text_dict:
            value = value + (frequency_inserted_dict[word] / frequency_new_text_dict[word])
    return ((1.0 + value) / (1.0 + len(inserted_dict)))

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
            inserted_words = diff_inserted_words(old_text, new_text)
            average_term_frequency = calculate_average_term_frequency(inserted_words, re.findall(r"[\w']+|[.,!?;]", new_text))
            values.append(average_term_frequency)
            T = T - 1
            if T == 0:
                break
        build_csv(values)
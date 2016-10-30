import csv
from search_file import find
from create_csv import initialize, build_csv
from edit import diff_inserted_words
from word_list import vulgar_words

def calculate_vulgarism_ratio(inserted_words):
    vulgar_word_list = vulgar_words()
    vulgar_words_count = 0
    for word in inserted_words:
        if word in vulgar_word_list:
            vulgar_words_count = vulgar_words_count + 1
    return 0.0 if not inserted_words else ((float)(vulgar_words_count) / len(inserted_words))

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
            vulgarism_ratio = calculate_vulgarism_ratio(inserted_words)
            values.append(vulgarism_ratio)
            T = T - 1
            if T == 0:
                break
    build_csv(values)
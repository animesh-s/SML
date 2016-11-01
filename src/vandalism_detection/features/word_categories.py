import csv
from search_file import find
from create_csv import initialize, build_csv
from edit import diff_inserted_words
from word_list import vulgar_words, biased_words, pronouns

def calculate_vulgarism_ratio(inserted_words):
    vulgar_word_list = vulgar_words()
    vulgar_words_count = 0
    for word in inserted_words:
        if word in vulgar_word_list:
            vulgar_words_count = vulgar_words_count + 1
    return 0.00 if not inserted_words else round(((float)(vulgar_words_count) / len(inserted_words)), 2)

def calculate_biased_ratio(inserted_words):
    biased_word_list = biased_words()
    biased_words_count = 0
    for word in inserted_words:
        if word in biased_word_list:
            biased_words_count = biased_words_count + 1
    return 0.00 if not inserted_words else round(((float)(biased_words_count) / len(inserted_words)), 2)

def calculate_pronoun_ratio(inserted_words):
    pronoun_word_list = pronouns()
    pronoun_words_count = 0
    for word in inserted_words:
        if word in pronoun_word_list:
            pronoun_words_count = pronoun_words_count + 1
    return 0.00 if not inserted_words else round(((float)(pronoun_words_count) / len(inserted_words)), 2)

def calculate_word_categories_ratios(inserted_words):
    lower_inserted_words = [word.lower() for word in inserted_words]
    vulgarism_ratio = calculate_vulgarism_ratio(lower_inserted_words)
    biased_ratio = calculate_biased_ratio(lower_inserted_words)
    pronoun_ratio = calculate_pronoun_ratio(lower_inserted_words)
    ratios = str(vulgarism_ratio) + ',' + str(biased_ratio) + ',' + str(pronoun_ratio) 
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
            inserted_words = diff_inserted_words(old_text, new_text)
            ratios = calculate_word_categories_ratios(inserted_words)
            values.append(ratios)
            T = T - 1
            if T == 0:
                break
    build_csv(values)
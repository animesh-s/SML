import csv
import scipy.stats as scs
from edit import diff_inserted_text, diff_inserted_words
from create_csv import initialize, build_csv
from search_file import find

def get_character_sequence_length(inserted_text):
    char_length_array = [0]*256

    for i in range(0,256):
        for j in range(0,len(inserted_text)):
            if chr(i) == inserted_text[j]:
                next_char = inserted_text[j]
                k = 0
                length = 0
                while(next_char == chr(i)):
                    length += 1
                    k += 1
                    if (j+k) >= len(inserted_text):
                        break
                    next_char = inserted_text[j+k]

                # check if length is greater than current max length
                if(length > char_length_array[i]):
                    char_length_array[i] = length

    return char_length_array

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
            inserted_words = diff_inserted_words(old_text,new_text)
            longest_char_seq_len = 0
            for word in inserted_words:
                if not word:
                    char_seq_len = 0
                else:
                    char_seq_len = max(get_character_sequence_length(word))
                if char_seq_len > longest_char_seq_len:
                    longest_char_seq_len = char_seq_len
            values.append(longest_char_seq_len)
            T = T - 1
            if T == 0:
                break
        build_csv(values)



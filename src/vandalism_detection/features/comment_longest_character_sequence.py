import csv
import os
from create_csv import initialize, build_csv
from longest_character_sequence import get_character_sequence_length

if __name__ == "__main__":
    values, T = initialize()
    with open('../../../../dataset/edits.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            comment = row['editcomment']
            if comment == 'null':
                comment = ''
            longest_char_seq_len = 0
            for word in comment.split():
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
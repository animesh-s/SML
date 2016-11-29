import csv
from edit import diff_inserted_text
from create_csv import initialize, build_csv
from search_file import find


def get_unique_char_count(inserted_text):
    char_arr = [0]*255
    for char in inserted_text:
        char_arr[ord(char)] = 1
    return sum(char_arr)

if __name__ == "__main__" :
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
            inserted_text = diff_inserted_text(old_text,new_text)
            length = len(inserted_text)
            if not inserted_text:
                diversity = 0
            else:
                unique_char_count = get_unique_char_count(inserted_text)    
                # not sure if needed
                if unique_char_count == 0:
                    diversity = 0
                else:
                    diversity = pow(len(inserted_text),1.0/unique_char_count)
            values.append(diversity)
            T = T - 1
            if T == 0:
                break
        build_csv(values)

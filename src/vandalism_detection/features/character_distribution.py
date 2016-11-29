import csv
import scipy.stats as scs
from edit import diff_inserted_text
from create_csv import initialize, build_csv
from search_file import find

def get_prob_dist(inserted_text):
    prob_dist = [0]*256
    for char in inserted_text:
        prob_dist[ord(char)] += 1

    return prob_dist

def get_entropy(prob_dist):
    return round(scs.entropy(prob_dist), 2)

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
            if not inserted_text:
                entropy = 0
            else:
                prob_dist = get_prob_dist(inserted_text)
                entropy = get_entropy(prob_dist)
            values.append(entropy)
            T = T - 1
            if T == 0:
                break
        build_csv(values)

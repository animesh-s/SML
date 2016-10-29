import csv
import re
from create_csv import initialize

def is_ip(editor):
    return 0 if (re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", editor) == None) else 1

def is_anonymous(editor):
    return is_ip(editor)

if __name__ == "__main__":
    values, T = initialize()
    num_points = T
    with open('../../../../dataset/edits.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            anonymous = is_anonymous(row['editor'])
            values.append(anonymous)
            T = T - 1
            if T == 0:
                break
    writer = open('../../../../features.csv', 'w')
    for i in range(num_points):
        writer.write(str(i+1) + ',' + str(values[i]) + '\n')
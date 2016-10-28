import csv
import re

def is_ip(editor):
    return 0 if (re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", editor) == None) else 1

def is_anonymous(editor):
    return is_ip(editor)

if __name__ == "__main__":
    values = []
    with open('../../../../dataset/edits.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            anonymous = is_anonymous(row['editor'])
            values.append(anonymous)
    with open('../../../../features.csv', 'w') as featuresfile:
        fieldnames = ['anonymous']
        writer = csv.DictWriter(featuresfile, fieldnames=fieldnames)
        writer.writeheader()
        for value in values:
            writer.writerow({'anonymous': value})
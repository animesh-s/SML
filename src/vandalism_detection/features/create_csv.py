import csv
import os

def initialize():
    values = []
    T = 32439
    return values, T

def build_csv(values):
    db = {}
    reader = csv.reader(open('../../../../features.csv', 'r'))
    for row in reader:
        key, data = row[0], row[1:]
        db[key] = ','.join(data)
    writer = open('../../../../new_features.csv', 'w')
    for key in sorted(map(int, db.keys())):
        writer.write(str(key) + ',' + db[str(key)] + ',' + str(values[key-1]) + '\n')
    os.remove('../../../../features.csv')
    os.rename('../../../../new_features.csv', '../../../../features.csv')
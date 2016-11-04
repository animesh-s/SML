import csv
import os

if __name__ == "__main__":
    db1 = {}
    db2 = {}
    count = 0
    reader1 = csv.reader(open('../../../../features.csv', 'r'))
    for row in reader1:
        key, data = row[0], row[1:]
        db1[key] = ','.join(data)
    reader2 = csv.reader(open('../../../../dataset/gold-annotations.csv', 'r'))
    for row in reader2:
        edit_id, data = row[0], row[1]
        data = '0' if data == 'regular' else '1'
        db2[str(count)] = ','.join([edit_id, data])
        count = count + 1
    writer = open('../../../../new_features.csv', 'w')
    for key in sorted(map(int, db1.keys())):
        edit_id, label = db2[str(key)].split(',')
        writer.write(edit_id + ',' + db1[str(key)] + ',' + label + '\n')
    os.remove('../../../../features.csv')
    os.rename('../../../../new_features.csv', '../../../../features.csv')
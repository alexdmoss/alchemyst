import csv
import json
from datetime import datetime
from collections import OrderedDict

csv_file = open('./pdf.csv', 'r')
json_file = open('./pdf.json', 'w')


json_file.write('{\n"entities": [\n')


fieldnames = ("doc_id", "type", "category", "level", "title", "description",
              "asset_link", "author", "last_modified", "filesize")
reader = csv.DictReader(csv_file, fieldnames)

count = 0

for row in reader:
    new_row = OrderedDict()
    for k, v in row.items():
        if k == 'doc_id':
            v = int(v)
        if k == 'title':
            if (type(v) == str):
                name = v.lower()
                name = name.replace(" ", "-")
                new_row['name'] = name
        if k == 'category':
            if (type(v) == str):
                category = v
                v = v.lower()
        if k == 'asset_link':
            if (type(v) == str):
                v = '/pdf/' + category + '/' + v
        if k == 'filesize':
            v = int(float(v) * 1024)
        if k == 'last_modified':
            dt = datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
            v = datetime.strftime(dt, '%Y-%m-%dT%H:%M:%S.000000')

        new_row['tags'] = []

        if k != 'type':
            new_row[k] = v

    if count != 0:
        json_file.write(',\n')

    json.dump(new_row, json_file)

    count = count + 1

json_file.write(']\n}\n')

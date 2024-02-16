"""
运行这个程序，导入example_data_1的数据。确保example_data_1.csv与这个文件在一起。
"""
import csv
import pymongo

with open('example_data_1.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = []
    for row in reader:
        row['age'] = int(row['age'])
        row['salary'] = int(row['salary'])
        row['id'] = int(row['id'])
        rows.append(row)

handler = pymongo.MongoClient().chapter_7.example_data_1
handler.insert_many(rows)

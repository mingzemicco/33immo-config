import csv
import pprint
import json
import time

from decimal import Decimal
from typing import List
import math


def to_numeric(input: str) -> int | float | None:
    if input is None: return None
    try:
        if input.isnumeric():
            return int(input)
        else:
            return float(input)
    except:
        return 0

def load_json(input: str):
    try:
        return json.loads(input)
    except:
        return None

def handle_row (row: object):
    id_ = row['id']
    link = row['link']
    department_id = row['department_id']
    title = row['title']
    zip_code = row['zip_code']
    
    description_en = row['description_en'].replace('_x000D_','') if row['description_en'] is not None else ''
    description_fr = row['description_fr'].replace('_x000D_','') if row['description_fr'] is not None else ''


    category = row['category']
    surface = to_numeric(row['surface'])
    price = to_numeric(row['price'])
    lower_price = to_numeric(row['lower_price'])
    upper_price = to_numeric(row['upper_price'])
    rent = row['rent']
    revenu = row['revenu']
    region = row['region']

    raw_images = row['images'].replace("'", '"').replace('\n', '').replace('\r', '')
    parsed_images = load_json(raw_images)
    images = list(filter(lambda it: len(it) > 0, parsed_images)) if isinstance(parsed_images, list) else []
    images = list(map(lambda it: it.replace('\n', ''), images))

    return {
        'surface': surface,
        'category': category,
        'lower_price': lower_price,
        'upper_price': upper_price,
        'rent': rent,
        'revenu': revenu,
        'region': region,
        'price': price,
        'images': images,
        'id': id_,
        'link': link,
        'department_id': department_id,
        'title': title,
        'zip_code': zip_code,
        'description_en': description_en,
        'description_fr': description_fr,
    }

def save_ids (ll):
    with open('saved_ids.txt', mode='a') as f:
        for it in ll:
            f.write(it['id']['S'] + '\n')

def read_saved_ids ():
    with open('saved_ids.txt', mode='r') as f:
        txt = f.read()
        return list(filter(lambda it: len(it) > 0, txt.split('\n')))

def write_csv(file_name: str, rows: List[object]):
    rows = list(map(lambda it: {
        'price': it['price'],
        'id': it['id'],
        'category': it['category'],
        'surface': it['surface'],
        'title': it['title'],
        'zip_code': it['zip_code'],
        'rent': it['rent']
    }, rows))
    with open(f'csv/{file_name}.csv', mode='w') as csv_file:
        first = rows[0]
        writer = csv.DictWriter(csv_file, fieldnames=first.keys())
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

with open('store.csv', mode='r') as f:
    rows = csv.DictReader(f)
    ll = []
    category_set = set()
    department_dict = {}
    for row in rows:
        parsed = handle_row(row)
        category_set.add(parsed['category'])
        department_id = parsed['department_id']
        if department_id in department_dict:
            department_dict[department_id].append(parsed)
        else:
            department_dict[department_id] = [parsed]
    split_size = 500
    json_obj = {}
    for department_id, rows in department_dict.items():
        cnt = 0
        json_obj[department_id] = { 'total_count': len(rows) }
        while (len(rows) > 0):
            _rows = rows[0:split_size]
            suffix = f'-{cnt}' if cnt > 0 else ''
            write_csv(f"{department_id}{suffix}", _rows)
            rows = rows[split_size:]
            cnt += 1
    with open('./csv/department_config.json', 'w') as f:
        json.dump(json_obj, f)


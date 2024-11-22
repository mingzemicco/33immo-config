import csv
from typing import List
import requests
import io
import re
import copy

pattern = r'[0-9]'

def download_department_csv (department_id: str):
    raw = requests.get(f'https://raw.githubusercontent.com/mingzemicco/33immo-config/refs/heads/main/department_postcodes/{department_id}.csv')
    text = raw.text
    rows = csv.DictReader(io.StringIO(text))
    ret = {}
    for row in rows:
        locality = re.sub(pattern, '', row['locality']).strip()
        latitude = row['latitude']
        longitude = row['longitude']
        postal_code = row['postal_code']
        obj = { 'latitude': latitude, 'longitude': longitude, 'postal_code': postal_code }
        if locality in ret:
            ret[locality].append(obj)
        else:
            ret[locality] = [obj]
    return ret

def find (city: str, items):
    for it in items:
        if city.startswith(it[0]):
            return it[1]
    print(f'{city} is not found')
    return None


def parse_names(cities: List[str], department_id: str):
    info = download_department_csv(department_id)
    d = info.items()
    ret = []
    for city in cities:
        objs = info[city] if city in info else find(city, d)
        if objs is not None:
            txt = "#".join(list(map(lambda it: f'{it['latitude']}${it['longitude']}${it['postal_code']}', objs)))
            ret.append(f'{city}({txt})')
        else:
            ret.append(city)
    return ret

with open('programe_department_cities.csv') as f:
    rows = csv.DictReader(f)
    ret = []
    for row in rows:
        cities = row['cities'].split('|')
        department_id = row['department_id']
        cities = parse_names(cities, department_id)
        cities_text = "|".join(cities)
        row['cities'] = cities_text
        ret.append(copy.copy(row))
    first = ret[0]
    with open('out.csv', mode='w') as out:
        writer = csv.DictWriter(out, fieldnames=first.keys())
        writer.writeheader()
        for row in ret:
            writer.writerow(row)
import csv

def read_file():
    with open('20230823-communes-departement-region.csv', mode='r') as csv_file:
        ret = []
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                nom_commune_complet = row['nom_commune_complet']
                code_departement = row['code_departement']
                nom_departement = row['nom_departement']
                code_postal = row['code_postal']
                code_departement = code_departement.zfill(2)
                code_postal = code_postal.zfill(5)
                latitude = row['latitude'][0:6]
                longitude = row['longitude'][0:6]
                ret.append({
                    'department_id': code_departement,
                    'department_name': nom_departement,
                    'latitude': latitude,
                    'longitude': longitude,
                    'locality': nom_commune_complet,
                    'postal_code': code_postal,
                })
        line_count += 1
        return ret
    
def write(department_id, rows):
    with open(f'department_postcodes/{department_id}.csv', mode='w') as csv_file:
        first = rows[0]
        writer = csv.DictWriter(csv_file, fieldnames=first.keys())
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
  
if __name__ == '__main__':
    rows = read_file()
    
    department_id_map = {}
    for row in rows:
        department_id = row['department_id']
        if department_id in department_id_map:
            department_id_map[department_id].append(row)
        else:
            department_id_map[department_id] = [row]
    for department_id, rows in department_id_map.items():
        write(department_id, rows)
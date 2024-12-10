import yaml
import csv
import re

def create_csv(yaml_path, csv_path):
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
        
    names = data.get('names', [])
    
    pattern = r'^([a-zA-Z0-9\.\-]+)_([a-zA-Z0-9\.\-]+)_([a-zA-Z0-9\.\-]+)_(\d{4}-\d{4}|\d{4})$'
    rows = []
    for item in names:
        match = re.match(pattern, item)
        if match:
            groups = [part.replace('-', ' ') for part in match.groups()]
            rows.append(groups)
            
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Make', 'Model', 'Variant', 'Year'])
        writer.writerows(rows)
        
yaml_path = r'Deployment\ImageDetection\data.yaml'
csv_path = r'Deployment\ImageDetection\autofil_data.csv'

create_csv(yaml_path, csv_path)

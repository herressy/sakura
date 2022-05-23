import os
import csv

from pathlib import Path

BASE_DIR = str(Path(__file__).resolve().parent.parent)
print(BASE_DIR)

menu_path = str(BASE_DIR) + '/menu/'
for file in os.listdir(menu_path):
    if file.endswith('.csv'):
        file_abs_path = menu_path + file
        with open(file_abs_path, 'r') as f:
            reader = csv.DictReader(f, delimiter=';')
            for line in reader:
                name = line['NAME']
                price = line['PRICE']
                kind = file.rsplit('.')[0]

                print(name, price, kind)

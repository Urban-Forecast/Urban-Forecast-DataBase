import json
import psycopg2
from fuzzywuzzy import process


# Функция обработки названий улиц
def beautiful_name(s_name):
    if 'Вишнёвая' in s_name or 'Надёжная' in s_name:
        s_name = s_name.replace('ё', 'е')
    if '(' in s_name:
        return s_name.split('(')[0]
    else:
        return s_name


# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="2335",
    database="OOP_database")
cursor = conn.cursor()

# Открытие json-файла и чтение данных
with open(r'files/addresses_v2.json', 'r', encoding='utf-8') as file:
    street_data = json.load(file)

# Открытие json-файла и чтение данных
with open(r'files/districts_v2.json', 'r', encoding='utf-8') as file:
    area_data = json.load(file)

areas_names = {'Западный район': 1, 'Карасунский район': 2, 'Прикубанский район': 3, 'Центральный район': 4}

# Внесение данных в базу данных
for keys in street_data.values():
    for street_name in keys.keys():
        for area, streets in area_data.items():
            matches = process.extractOne(beautiful_name(street_name), streets)
            if matches[1] >= 95:
                area_id = areas_names.get(area)
                print('\n street_name:', street_name,      # Название проверяемой улицы из файла с домами
                      '\n street:', matches[0],            # Название улицы из файла с районами для сравнения
                      '\n matches:', matches[1],           # Степень совпадения названий улиц, указанных выше
                      '\n area:', area,                    # Название района, к которому относится проверяемая улица
                      '\n area_id:', area_id)              # Id района, к которому относится проверяемая улица
                cursor.execute('''INSERT INTO "OOP_database".streets (street_name, area_id) VALUES (%s, %s) ;''',
                (street_name, area_id))

# Сохранение изменений и закрытие соединения с базой данных
conn.commit()
cursor.close()
conn.close()

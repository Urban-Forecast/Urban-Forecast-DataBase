import json
import psycopg2
from fuzzywuzzy import process

# подключаем модуль datetime
import datetime

# фиксируем и выводим время старта работы кода
start = datetime.datetime.now()
print('Время старта: ' + str(start))

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
with open(r'files/buildings_info_domreestr.json', 'r', encoding='utf-8') as file:
    build_data = json.load(file)

# Открытие json-файла и чтение данных
with open(r'files/coordinates_overpass.json', 'r', encoding='utf-8') as file:
    coord_data = json.load(file)

# Внесение данных в базу данных
complete = 0
miss = 0
for streets in build_data.values():
    for street_name, houses in streets.items():
        # Поиск соответствующего значения id в таблице streets
        cursor.execute('''SELECT id, street_name, area_id FROM "OOP_database".streets''')
        results = cursor.fetchall()
        matches = process.extractOne(street_name, [result[1] for result in results])
        if matches[1] >= 90:  # Пороговое значение для считывания совпадений
            street_id = [result[0] for result in results if result[1] == matches[0]][0]
            area_id = [result[2] for result in results if result[1] == matches[0]][0]
            complete += 1
            # print(f"{street_name}\n{matches[0]}\nСовпадение: {matches[1]} %\nid = {street_id}\n")
            if houses is not None:
                for address_number, house_info in houses.items():
                    # print(address_number)
                    if house_info is not None:
                        square = house_info.get("Общая площадь, кв.м")
                        if square:
                            square = float(square.replace(' ', '').replace(',', '.'))
                        live_square = house_info.get("Общая площадь жилых помещений, кв.м")
                        if live_square:
                            live_square = float(live_square.replace(' ', '').replace(',', '.'))
                        floors = house_info.get("Количество этажей, ед.")
                        people = house_info.get("Численность жителей, чел.")
                        if people is None and live_square is not None:
                            people = live_square * 0.077
                        # Вставка данных в таблицу builds
                        cursor.execute('''INSERT INTO "OOP_database".builds 
                            (address_number, street_id, area_id, square, floors, 
                            people, live_square)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                            (address_number, street_id, area_id, square, floors,
                             people, live_square))
        else:
            miss += 1
            print("Street not found\n")

print("Есть совпадение (>= 90%):", complete)
print("Нет совпадения (меньше 90%):", miss)

# Сохранение изменений и закрытие соединения с базой данных
conn.commit()
cursor.close()
conn.close()

# фиксируем и выводим время окончания работы кода
finish = datetime.datetime.now()
print('Время окончания: ' + str(finish))

# вычитаем время старта из времени окончания
print('Время работы: ' + str(finish - start))

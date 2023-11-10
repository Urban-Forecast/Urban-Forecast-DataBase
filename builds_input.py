import json
import psycopg2
from fuzzywuzzy import process

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="2335",
    database="OOP_database")
cursor = conn.cursor()

# Открытие json-файла и чтение данных
with open(r'files/buildings_info.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Внесение данных в базу данных
for num, streets in data.items():
    for street_name, houses in streets.items():
        print(street_name)
        # Поиск соответствующего значения id в таблице streets
        cursor.execute('''SELECT street_name, id FROM "OOP_database".streets''')
        results = cursor.fetchall()
        matches = process.extractOne(street_name, [result[0] for result in results])
        if matches[1] > 90:  # Пороговое значение для считывания совпадений
            street_id = [result[1] for result in results if result[0] == matches[0]][0]
            print("id = ", street_id)
        else:
            print("Street not found")
        print("\n")
        """if houses is not None:
            for house_num, house_info in houses.items():
                print(house_num)
                for key, value in house_info.items():
                    print(key, value)
                    if key == "Общая площадь, кв.м":
                        square = value
                        if not value:
                            square = None
                    if key == "Общая площадь жилых помещений, кв.м":
                        live_square = value
                        if not value:
                            live_square = None
                    if key == "Количество этажей, ед.":
                        floors = value
                        if not value:
                            floors = None
                    if key == "Численность жителей, чел.":
                        people = value
                        if not value:
                            people = None
                    if key == "Количество подъездов, ед.":
                        entrance = value
                        if not value:
                            entrance = None
                # Вставка данных в таблицу builds
                cursor.execute(
                    '''INSERT INTO "OOP_database".builds 
                    (adres_number, street_id, square, floors, entrance, people, live_square) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                    (house_num, street_id, square, floors, entrance, people, live_square))"""

# Сохранение изменений и закрытие соединения с базой данных
conn.commit()
cursor.close()
conn.close()

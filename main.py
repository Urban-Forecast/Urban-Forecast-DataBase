import json
import psycopg2
from fuzzywuzzy import process

# Подключение к базе данных
# Connection to database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="2335",
    database="OOP_database")
cursor = conn.cursor()

# Открытие json-файла и чтение данных
# Open json-file and read data
with open(r'files/buildings_info.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

nesto = 0
sto = 0
miss = 0
# Внесение данных в базу данных
# Insert data in database
for num, streets in data.items():
    for street_name, houses in streets.items():
        # Поиск соответствующего значения id в таблице streets
        cursor.execute('''SELECT street_name, id FROM "OOP_database".streets''')
        results = cursor.fetchall()
        matches = process.extractOne(street_name, [result[0] for result in results])
        if matches[1] >= 90:  # Пороговое значение для считывания совпадений
            street_id = [result[1] for result in results if result[0] == matches[0]][0]
            if matches[1] != 100:
                nesto += 1
                print(street_name)
                print(matches[0])
                print("Совпадение: ", matches[1], "%")
                print("id = ", street_id)
                print("")
            if matches[1] == 100:
                sto += 1
        else:
            miss += 1
            print("Street not found")
            print("")
print("Не стопроцентное совпадение: ", nesto)
print("Стопроцентное совпадение:", sto)
print("Нет совпадения (меньше 90%):", miss)

# Сохранение изменений и закрытие соединения с базой данных
# Save changes and close connection to database
conn.commit()
cursor.close()
conn.close()

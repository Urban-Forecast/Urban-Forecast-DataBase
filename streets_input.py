import json
import psycopg2

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
    data = json.load(file)

# Внесение данных в базу данных

for v in data.values():
    for i, j in v.items():
        cursor.execute('''INSERT INTO "OOP_database".streets (street_name) VALUES (%s) ;''', (i,))

# Сохранение изменений и закрытие соединения с базой данных
conn.commit()
cursor.close()
conn.close()

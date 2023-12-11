import json
import psycopg2
from fuzzywuzzy import process

# подключаем модуль datetime
import datetime

# фиксируем и выводим время старта работы кода
start = datetime.datetime.now()
print('Время старта: ' + str(start))

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="2335",
    database="OOP_database")
cursor = conn.cursor()

# Открытие json-файла и чтение данных
with open(r'files/coordinates_overpass.json', 'r', encoding='utf-8') as file:
    coord_data = json.load(file)
count = 0
b_count = 0
for streets, adrs in coord_data.items():
    for nums, locate in adrs.items():
        locate_1, locate_2 = round(locate[0], 5), round(locate[1], 5)
        build_id = None
        cursor.execute(f'''SELECT street_name, id FROM "OOP_database".streets WHERE street_name = '{streets}';''')
        s_results = cursor.fetchall()
        if s_results != []:
            street_id = s_results[0][1]
            """print("ififififif")
            print("s_results = ", s_results)
            print("s_results[0] = ", s_results[0])
            print("s_results[1] = ", s_results[0][1])
            print("street_id = ", street_id)"""
            cursor.execute(f'''SELECT id FROM "OOP_database".builds 
            WHERE street_id = '{street_id}' AND address_number = '{nums}';''')
            b_results = cursor.fetchall()
            count += 1
            if b_results != []:
                build_id = b_results[0][0]
                b_count += 1
            address = streets + " " + nums
            cursor.execute('''INSERT INTO "OOP_database".coords (address, build_id, locate_1, locate_2) 
            VALUES (%s, %s, %s, %s) ;''', (address, build_id, locate_1, locate_2))
            """print('\n streets: ', streets,
                  '\n address: ', address,
                  '\n nums: ', nums,
                  '\n coords: ', locate,
                  '\n locate_1: ', locate_1,
                  '\n locate_2: ', locate_2,
                  '\n build_id: ', build_id)"""
        else:
            # print("elseelseelse")
            address = streets + " " + nums
            cursor.execute('''INSERT INTO "OOP_database".coords (address, build_id, locate_1, locate_2) 
            VALUES (%s, %s, %s, %s) ;''', (address, build_id, locate_1, locate_2))
            """print('\n streets: ', streets,
                  '\n address: ', address,
                  '\n nums: ', nums,
                  '\n coords: ', locate,
                  '\n locate_1: ', locate_1,
                  '\n locate_2: ', locate_2,
                  '\n build_id: ', build_id)"""
print("count = ", count)
print("b_count = ", b_count)
# Сохранение изменений и закрытие соединения с базой данных
conn.commit()
cursor.close()
conn.close()

# фиксируем и выводим время окончания работы кода
finish = datetime.datetime.now()
print('Время окончания: ' + str(finish))

# вычитаем время старта из времени окончания
print('Время работы: ' + str(finish - start))

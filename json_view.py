import json


# Просмотр файла с адресами
def street_view():
    # Открытие json-файла и чтение данных
    with open(r'files/addresses_v2.json', 'r', encoding='utf-8') as file:
        street_data = json.load(file)

    # Только улицы
    for v in street_data.values():
        for i, j in v.items():
            print(i)
# ************************


# Просмотр файла с районами
def areas_view(num):
    # Открытие json-файла и чтение данных
    with open(r'files/districts_v2.json', 'r', encoding='utf-8') as file:
        area_data = json.load(file)

    # Районы и улицы в красивом виде
    if num == 1:
        for k, v in area_data.items():
            print(k, ": ", ", ".join(v))

    # Районы и улицы в виде словарей
    if num == 2:
        for k in area_data.items():
            print(k)

    # Только районы
    if num == 3:
        for k in area_data.keys():
            print(k)
# ************************


# Просмотр файла с домами
def build_view():
    # Открытие json-файла и чтение данных
    with open(r'files/buildings_info.json', 'r', encoding='utf-8') as file:
        build_data = json.load(file)

    # Просмотр от улиц
    for k, v in build_data.items():
        print("k = ", k, "\n")
        for s in v.items():
            print("in items", s)
        print("\n\n")
        for s in v.values():
            print("in values", s)
        print("\n\n")


def iterate_json():
    # Открытие json-файла и чтение данных
    with open(r'files/buildings_info.json', 'r', encoding='utf-8') as file:
        build_data = json.load(file)
    for streets in build_data.values():
        for street_name, houses in streets.items():
            print(street_name)
            if houses is not None:
                for house_num, house_info in houses.items():
                    print(house_num)
                    if house_info is not None:
                        for key, value in house_info.items():
                            print(key, value)


iterate_json()
# ************************


# Просмотр файла с координатами
def coord_view():
    # Открытие json-файла и чтение данных
    with open(r'files/coordinates_overpass.json', 'r', encoding='utf-8') as file:
        coord_data = json.load(file)

    # Всё
    for streets, adrs in coord_data.items():
        for nums, coords in adrs.items():
            print('\n streets:', streets,
                  '\n adrs:', adrs,
                  '\n nums:', nums,
                  '\n coords:', coords)

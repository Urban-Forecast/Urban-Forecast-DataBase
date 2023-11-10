import json

#Просмотр файла с адресами
'''
with open(r'files/addresses_v2.json', 'r') as openfile:
    j_object = json.load(openfile)
print(j_object)

# Только улицы
for v in j_object.values():
    for i, j in v.items():
        print(i)
'''
# ************************

# Просмотр файла с районами
'''
with open(r'files/districts_v2.json', 'r') as openfile:
    j_object = json.load(openfile)
print(j_object)

# Районы и улицы в красивом виде
for k, v in j_object.items():
    print(k, ": ", ", ".join(v))

# Районы и улицы в виде словарей
for k in j_object.items():
    print(k)
    
# Только районы
for k in j_object.keys():
    print(k)
'''
# ************************

# Просмотр файла с домами

with open(r'files/buildings_info.json', 'r') as openfile:
    data = json.load(openfile)
print(data)

# Просмотр от улиц
for k, v in data.items():
    print("k = ", k, "\n")
    for s in v.items():
        print("in items", s)
    print("\n\n")
    for s in v.values():
        print("in values", s)
    print("\n\n")
def iterate_json(data):
    for num, streets in data.items():
        for street_name, houses in streets.items():
            print(street_name)
            if houses is not None:
                for house_num, house_info in houses.items():
                    print(house_num)
                    for key, value in house_info.items():
                        print(key, value)

#iterate_json(data)
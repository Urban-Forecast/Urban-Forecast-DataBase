from fuzzywuzzy import fuzz
from fuzzywuzzy import process

a = fuzz.partial_ratio('4-я Тихая', '4-я Тихая улица')
print(a)

a = fuzz.token_sort_ratio('4-я Тихая', '4-я Тихая улица')
print(a)
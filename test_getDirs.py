import requests

print(requests.get('http://127.0.0.1:5000/getDirs',
                                params={'login': 'zubkova', 'password': '12345'}).json())
a = {'1': 1, '2': 2,
     '3': {
         '4': 4,
         '5': 5,
         '6': 6
     }}
print(len(a))
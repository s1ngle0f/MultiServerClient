import os
import json


path = 'C:/Users/zubko/Desktop/docx'

def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir(path)]
    else:
        d['type'] = "file"
    return d

print(json.dumps(path_to_dict(path)))
print(path_to_dict(path), type(path_to_dict(path)))

a = {'1': 1,
     '2': 2}

b = {'1': 1,
     '2': 2}

print(a == b)
print('123' == '123')
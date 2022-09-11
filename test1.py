import dictdiffer
import os
import json
import directory_tree
a = {'children': [
              {'children': [{'name': 'docccss.docx',
                             'path': '/docx/otchet/docccss.docx',
                             'time': 1661377954.9258397,
                             'type': 'file'}],
               'name': 'otchet',
               'path': '/docx/otchet',
               'type': 'directory'},
              {'children': [{'children': [{'name': 'ugabuga.txt',
                                           'path': '/docx/test/test2/ugabuga.txt',
                                           'time': 1661377554.2848547,
                                           'type': 'file'}],
                             'name': 'test2',
                             'path': '/docx/test/test2',
                             'type': 'directory'}],
               'name': 'test',
               'path': '/docx/test',
               'type': 'directory'},
              {'children': [{'name': 'Microsoft Access Database.accdb',
                             'path': '/docx/Новая папка/Microsoft Access '
                                     'Database.accdb',
                             'time': 1661625352.9123597,
                             'type': 'file'}],
               'name': 'Новая папка',
               'path': '/docx/Новая папка',
               'type': 'directory'},
              {'children': [],
               'name': 'Новая папка (2)',
               'path': '/docx/Новая папка (2)',
               'type': 'directory'},
              {'name': 'приемка.docx',
               'path': '/docx/приемка.docx',
               'time': 1661714051.214494,
               'type': 'file'},
              # {'name': 'Текстовый документ.txt',
              #  'path': '/docx/Текстовый документ.txt',
              #  'time': 1661714063.5165775,
              #  'type': 'file'}
                ],
 'name': 'docx',
 'path': '/docx',
 'type': 'directory'}

b = {'children': [
              {'children': [{'name': 'docccss.docx',
                             'path': '/docx/otchet/docccss.docx',
                             'time': 1661377954.9258321397, #Edit
                             'type': 'file'}],
               'name': 'otchet',
               'path': '/docx/otchet',
               'type': 'directory'},
              {'children': [{'children': [{'name': 'ugabuga.txt',
                                           'path': '/docx/test/test2/ugabuga.txt',
                                           'time': 1661377554.2848547,
                                           'type': 'file'}],
                             'name': 'test2',
                             'path': '/docx/test/test2',
                             'type': 'directory'}],
               'name': 'test',
               'path': '/docx/test',
               'type': 'directory'},
              {'children': [{'name': 'Microsoft Access Database.accdb',
                             'path': '/docx/Новая папка/Microsoft Access '
                                     'Database.accdb',
                             'time': 1661625352.911237, #Edit
                             'type': 'file'}],
               'name': 'Новая папка',
               'path': '/docx/Новая папка',
               'type': 'directory'},
              # {'children': [],
              #  'name': 'Новая папка (2)',
              #  'path': '/docx/Новая папка (2)', #Deleted
              #  'type': 'directory'},
              {'name': 'приемка.docx',
               'path': '/docx/приемкasdав.docx', #Edit
               'time': 1661714051.214494,
               'type': 'file'},
              {'name': 'Текстовый документ.txt',
               'path': '/docx/Текстовый документ.txt',
               'time': 1661714063.5165775,
               'type': 'file'}],
 'name': 'docx',
 'path': '/docx',
 'type': 'directory'}

# cort = ('change', 'key', ('val', 'val0'))
# print(cort[0])

# def findDifferentForSending(last_tree, current_tree):
#     change = []
#     remove = []
#     for diff in list(dictdiffer.diff(last_tree, current_tree)):
#         print(diff)
#         if type(diff[1]) == list:
#             if diff[0] == 'change':
#                 tmp = current_tree
#                 for i, val in enumerate(diff[1]):
#                     if i == len(diff[1]) - 1:
#                         change.append(tmp.get('path'))
#                     if type(tmp) == dict:
#                         tmp = tmp.get(val)
#                     elif type(tmp) == list:
#                         tmp = tmp[int(val)]
#             elif diff[0] == 'remove':
#                 tmp = last_tree
#                 for i, val in enumerate(diff[1]):
#                     if type(tmp) == dict:
#                         tmp = tmp.get(val)
#                     elif type(tmp) == list:
#                         tmp = tmp[int(val)]
#                     if i == len(diff[1]) - 1:
#                         print('DEBUG', tmp)
#                         remove.append(tmp.get('path'))
#             elif diff[0] == 'add': #Не сделал этот сектор
#                 tmp = current_tree
#                 for i, val in enumerate(diff[1]):
#                     if type(tmp) == dict:
#                         tmp = tmp.get(val)
#                     elif type(tmp) == list:
#                         tmp = tmp[int(val)]
#                     if i == len(diff[1]) - 1:
#                         print('DEBUG', tmp)
#                         remove.append(tmp.get('path'))
#         # print(last_tree[diff[1][0]][diff[1][1]])
#         print(tmp)
#     return {'change': list(set(change)),
#             'remove': list(set(remove))
#             }

base_dir = 'C:/Users/zubko/Desktop/'
main_path = base_dir + 'docx'
settings_path = os.getenv('APPDATA') + '/MultiFolder/settings.json'


def findDifferentForSending(last_tree, current_tree):
    change = []
    remove = []
    for diff in list(dictdiffer.diff(last_tree, current_tree)):
        print(diff)
        if type(diff[1]) == list:
            if diff[0] == 'change':
                tmp = current_tree
                for i, val in enumerate(diff[1]):
                    if i == len(diff[1]) - 1:
                        change.append(tmp.get('path'))
                    if type(tmp) == dict:
                        tmp = tmp.get(val)
                    elif type(tmp) == list:
                        tmp = tmp[int(val)]
            elif diff[0] == 'remove':
                tmp = last_tree
                for i, val in enumerate(diff[1]):
                    if type(tmp) == dict:
                        tmp = tmp.get(val)
                    elif type(tmp) == list:
                        tmp = tmp[int(val)]
                    if i == len(diff[1]) - 1:
                        print('DEBUG', tmp)
                        remove.append(tmp.get('path'))
            elif diff[0] == 'add': #Не сделал этот сектор
                tmp = current_tree
                for i, val in enumerate(diff[1]):
                    if type(tmp) == dict:
                        tmp = tmp.get(val)
                    elif type(tmp) == list:
                        tmp = tmp[int(val)]
                    if i == len(diff[1]) - 1:
                        print('DEBUG', tmp)
                        remove.append(tmp.get('path'))
        # print(last_tree[diff[1][0]][diff[1][1]])
        print(tmp)
    return {'change': list(set(change)),
            'remove': list(set(remove))
            }

# print(findDifferentForSending(a, b))

# print(directory_tree.get_files_and_time_full_path(main_path))
# print(directory_tree.get_files_and_time(main_path, base_dir=base_dir))

# last_scan = {}
# if last_scan == None:
#     print(123)

if not os.path.exists(settings_path):
    if not os.path.exists(settings_path[:settings_path.rfind('/')]):
        os.makedirs(settings_path[:settings_path.rfind('/')])
    with open(settings_path, 'w', encoding='utf-8') as f:
        data = {'login': None, 'directories': []}
        json.dump(data, f, ensure_ascii=False, indent=4)
        settings = data
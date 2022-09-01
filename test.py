import time

import directory_tree
import requests
import dictdiffer
from threading import Thread


# base_dir = 'C:/Users/zubko/Desktop/'
# main_path = base_dir + 'docx'

def thread(d):
    while True:
        print(d['k'])
        time.sleep(3)

d = {"k": 'v'}

th = Thread(target=thread, args=(d,))
th.start()

while True:
    d['k'] += 'v'
    time.sleep(3)

print()

# server_files = requests.get('http://127.0.0.1:5000/getFilesArray',
#                    params={'login': 'zubkov', 'password': '12345', 'folder_name': 'docx'}).json()
# local_files = directory_tree.get_files_folder(main_path, base_dir)
#
# print(directory_tree.get_files_folder_and_size(main_path, base_dir))
# print(server_files)
# print(local_files)
#
# # print(list(dictdiffer.diff(server_files[1:], local_files)))
# def compareLists(first, second):
#     add = []
#     remove = []
#     for i in first:
#         if not(i in second):
#             remove.append(i)
#     for i in second:
#         if not(i in first):
#             add.append(i)
#     return {'add': add,
#             'remove': remove}
#
# print(compareLists(local_files, server_files[1:]))

# a = [1, 2, 3, 4]
# b = [2, 3, 4]
#
# print(compareLists(a, b))
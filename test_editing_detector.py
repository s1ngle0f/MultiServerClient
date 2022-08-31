import os
from pprint import pprint
import json
from flask import jsonify
import directory_tree
from time import sleep

base_dir = 'C:/Users/zubko/Desktop'
data_path = base_dir + '/docx'
doc = '/Текстовый документ.txt'

# tree['children'][5]['time'] = 1203
# pprint(tree)
# pprint(os.path.getatime(path + doc))

def findDifferentForSending(client_tree, server_tree):
    recieve = []
    for i in server_tree:
        if i not in client_tree:
            recieve.append(i)
    return recieve

def getPathsOfTree(tree, path = '', arr = None):
    if arr == None:
        arr = []
    if tree['type'] == 'directory':
        for i, child in enumerate(tree['children']):
            arr.append((path + '/' + child['name']).replace(data_path, ''))
            # print(path + '/' + child['name'])
            if child['type'] == 'directory':
                getPathsOfTree(child, path + '/' + child['name'], arr)
    return arr

tree = directory_tree.path_to_dict_with_time_and_path(data_path, base_dir=base_dir)
pprint(tree)

# last_tree = None
# while True:
#     sleep(5)
#     tree = directory_tree.path_to_dict_with_time_and_path(data_path, base_dir=base_dir)
#
#     # if last_tree != None and last_tree != tree:
#
#
#     last_tree = tree

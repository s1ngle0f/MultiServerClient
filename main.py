import requests
import directory_tree
import os
import dictdiffer
from time import sleep

base_dir = 'C:/Users/zubko/Desktop/insideFolderForConnection/'
main_path = base_dir + 'excel'
# print(requests.post('http://127.0.0.1:5000/upload', files={'document': file}, params={'login': 'zubkov', 'password': '12345'}).text)
# print(requests.post('http://127.0.0.1:5000/equalTree', params={'login': 'zubkov', 'password': '12345'}, json=tree).text)
# print(requests.get('http://127.0.0.1:5000/getTree', params={'login': 'zubkov', 'password': '12345', 'folder_name': 'docx'}).text)
# print(requests.post('http://127.0.0.1:5000/deleteNonExistentFoldersOrFiles', params={'login': 'zubkov', 'password': '12345', 'folder_name': 'docx'}, json=tree).text)

filename = main_path + 'doc.docx'
tree = directory_tree.path_to_dict(main_path)

timeUpdate = 5

def isExistFolder(path):
    base_dir = path[:path.rfind('/') + 1]
    dir = path.replace(base_dir, '')
    return requests.get('http://127.0.0.1:5000/isExistFolder',
                       params={'login': 'zubkov', 'password': '12345', 'folder_name': dir}).json()

def syncingWithServer(path):
    base_dir = path[:path.rfind('/')+1]
    dir = path.replace(base_dir, '')
    if not os.path.exists(path):
        os.makedirs(path)
        print('Created!')
    tree = directory_tree.path_to_dict(path)
    equlsTree = requests.post('http://127.0.0.1:5000/equalTree', params={'login': 'zubkov', 'password': '12345'}, json=tree).json()
    server_files_sizes = requests.get('http://127.0.0.1:5000/getFilesSize', params={'login': 'zubkov', 'password': '12345', 'folder_name': dir}).json()
    client_files_sizes = directory_tree.get_files_folder_and_size(path, base_dir)
    print(server_files_sizes)
    print(client_files_sizes)
    if equlsTree['isEquals'] == True:
        for diff in list(dictdiffer.diff(server_files_sizes, client_files_sizes)):
            print(diff)
            if diff[0] == 'change':
                if type(diff[1]) == str and diff[1].find('.') != -1:
                    print('CHANGE:', base_dir + diff[1])
                    tmp = diff[1]
                elif diff[1][0].find('.') != -1:
                    print('CHANGE:', base_dir + diff[1][0])
                    tmp = diff[1][0]
                file = requests.get('http://127.0.0.1:5000/getFile',
                                    params={'login': 'zubkov', 'password': '12345', 'folder_name': '', 'path': tmp},
                                    json=tree)
                with open(base_dir + tmp, 'wb') as f:
                    f.write(file.content)
    else:
        #удаление ненужных файлов и папок
        server_files = requests.get('http://127.0.0.1:5000/getFilesArray',
                                    params={'login': 'zubkov', 'password': '12345', 'folder_name': 'docx'}).json()
        local_files = directory_tree.get_files_folder(path, base_dir)
        remove_list = compareLists(local_files, server_files)['remove']
        add_list = compareLists(local_files, server_files)['add']
        for file_path in remove_list:
            try:
                if os.path.isdir(base_dir + file_path):
                    os.removedirs(base_dir + file_path)
                else:
                    os.remove(base_dir + file_path)
            except:
                print(base_dir + file_path)
                print('Error')
        # for file_path in add_list:
        #     isFile = str(file_path).rfind('.') != -1
        #     print(file_path, isFile)
        #     if not isFile:
        #         os.makedirs(base_dir + file_path)
        #     else:
        #         file = requests.get('http://127.0.0.1:5000/getFile',
        #                             params={'login': 'zubkov', 'password': '12345', 'folder_name': '', 'path': file_path},
        #                             json=tree)
        #         with open(base_dir + file_path, 'wb') as f:
        #             f.write(file.content)
        getMissingFiles(dir, base_dir)
        print('SYNC!')

def compareLists(first, second):
    add = []
    remove = []
    for i in first:
        if not(i in second):
            remove.append(i)
    for i in second:
        if not(i in first):
            add.append(i)
    return {'add': add,
            'remove': remove}

def detectChangesInFolder(path):
    base_dir = path[:path.rfind('/') + 1]
    dir = path.replace(base_dir, '')
    last_scan = directory_tree.get_files_folder_and_time(path, base_dir=base_dir)
    while True:
        scan = directory_tree.get_files_folder_and_time(path, base_dir=base_dir)
        # print(scan)
        for diff in list(dictdiffer.diff(last_scan, scan)):
            print(diff)
            if diff[0] == 'add':
                for file_path in diff[2]:
                    print('ADD:', base_dir + file_path[0])
                    if file_path[0].find('.') != -1:
                        with open(base_dir + file_path[0], 'rb') as file:
                            print(requests.post('http://127.0.0.1:5000/upload', files={'document': file},
                                                params={'login': 'zubkov', 'password': '12345', 'path': file_path[0]}).text)
                    else:
                        print(requests.post('http://127.0.0.1:5000/createFolders',
                                            params={'login': 'zubkov', 'password': '12345', 'path': file_path[0]}).text)
            elif diff[0] == 'remove':
                for file_path in diff[2]:
                    print('REMOVE:', base_dir + file_path[0])
                    print(requests.get('http://127.0.0.1:5000/delete',
                                       params={'login': 'zubkov', 'password': '12345', 'path': file_path[0]}).text)
            elif diff[0] == 'change':
                if type(diff[1]) == str and diff[1].find('.') != -1:
                    print('CHANGE:', base_dir + diff[1])
                    tmp = diff[1]
                elif diff[1][0].find('.') != -1:
                    print('CHANGE:', base_dir + diff[1][0])
                    tmp = diff[1][0]
                with open(base_dir + tmp, 'rb') as file:
                    print(requests.post('http://127.0.0.1:5000/upload', files={'document': file},
                                        params={'login': 'zubkov', 'password': '12345', 'path': tmp}).text)
        last_scan = scan
        sleep(timeUpdate)
# detectChangesInFolder(main_path)

# print(requests.get('http://127.0.0.1:5000/getLastTimeModification', params={'login': 'zubkov', 'password': '12345', 'folder_name': 'docx'}).text)
# print(getLastTimeModification(main_path))

def getLastTimeModification(path):
    base_dir = path[:path.rfind('/') + 1]
    dir = path.replace(base_dir, '')
    scan = directory_tree.get_files_folder_and_time(path, base_dir=base_dir)
    return sorted(scan.values())[-1]

def getMissingFiles(dir, base_dir):
    recieve = requests.post('http://127.0.0.1:5000/getListOfMissingObjects',
                            params={'login': 'zubkov', 'password': '12345', 'folder_name': dir}, json=tree).json()
    print(recieve)
    for i in recieve:
        isFile = str(i).rfind('.') != -1
        print(i, isFile)
        if not isFile:
            os.makedirs(base_dir + dir + i)
        else:
            file = requests.get('http://127.0.0.1:5000/getFile',
                                params={'login': 'zubkov', 'password': '12345', 'folder_name': dir, 'path': i}, json=tree)
            with open(base_dir + dir + i, 'wb') as f:
                f.write(file.content)

# getMissingFiles()

def uploadAllFiles(path):
    base_dir = path[:path.rfind('/') + 1]
    dir = path.replace(base_dir, '')
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            filelist.append(str(os.path.join(root, file)).replace('\\', '/'))
    print(filelist)
    for file in filelist:
        path_to_db = file.replace(base_dir, '')
        with open(file, 'rb') as file:
            print(requests.post('http://127.0.0.1:5000/upload', files={'document': file},
                                params={'login': 'zubkov', 'password': '12345', 'path': path_to_db}).text)

# uploadAllFiles(main_path)

def createFolders(path):
    base_dir = path[:path.rfind('/') + 1]
    dir = path.replace(base_dir, '')
    dirlist = []
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            dirlist.append(str(os.path.join(root, dir)).replace('\\', '/'))
    print(dirlist)
    for dir in dirlist:
        path_to_db = dir.replace(base_dir, '')
        # print(path_to_db)
        print(requests.post('http://127.0.0.1:5000/createFolders',
                            params={'login': 'zubkov', 'password': '12345', 'path': path_to_db}).text)
# print(createFolders(main_path))

def start(path):
    base_dir = path[:path.rfind('/') + 1]
    dir = path.replace(base_dir, '')
    if isExistFolder(path):
        serverLTM = requests.get('http://127.0.0.1:5000/getLastTimeModification',
                                params={'login': 'zubkov', 'password': '12345', 'folder_name': dir}, json=tree).json()
        localLTM = getLastTimeModification(path)
        if localLTM > serverLTM:
            uploadAllFiles(path)
            createFolders(path)
        else:
            syncingWithServer(path)
    else:
        uploadAllFiles(path)
        createFolders(path)
    detectChangesInFolder(path)

start(main_path)


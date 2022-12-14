import os
import pprint
import tkinter.filedialog
from threading import Thread
from tkinter import *
from tkinter import messagebox
import main
import requests
from main import start
import json
from functools import partial

folders = [
    'C:/Users/zubko/Desktop/docx',
    'C:/Users/zubko/Desktop/insideFolderForConnection/excel',
    'C:/Users/zubko/Desktop/pwpt'
]

# main.LOGIN = 'zubkova'

settings_path = os.path.abspath(os.curdir) + '/settings.json'

directories_el = {} #НЕ ТРОГАТЬ
server_dirs_el = {} #НЕ ТРОГАТЬ
settings = None

window = Tk()
window.title('MultiFolder')
window.geometry('800x600')

frame = Frame(
    window, #Обязательный параметр, который указывает окно для размещения Frame.
    padx = 10, #Задаём отступ по горизонтали.
    pady = 10 #Задаём отступ по вертикали.
)
frame.pack(expand=True)

def edit_login():
    new_login = height_tf.get()
    with open(settings_path, 'r+') as f:
        data = json.load(f)
        data['login'] = new_login  # <--- add `id` value.
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part

def updateSettings():
    global settings
    if not os.path.exists(settings_path):
        with open(settings_path, 'w', encoding='utf-8') as f:
            data = {'login': None, 'directories': []}
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
            print(settings)


updateSettings()
main.LOGIN = settings['login']
MAIN_DIRECTORIES = list(settings['directories']) if settings['directories'] != None else []


for i in MAIN_DIRECTORIES:
    th = Thread(target=start, args=(i, MAIN_DIRECTORIES))
    # threads[i] = th
    th.start()

def deleteDirectoryFromSettings(path):
    global directories_el
    with open(settings_path, 'r+') as f:
        data = json.load(f)
        for i, dir in enumerate(data['directories']):
            if dir == path:
                data['directories'].remove(dir)
                for obj in directories_el[dir]:
                    obj.destroy()
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part
    MAIN_DIRECTORIES.remove(path)
    print(path)

def createNewDir(dir):
    file_name = tkinter.filedialog.askdirectory()
    os.makedirs(file_name + '/' + dir)
    addDirectoryToSettings(file_name + '/' + dir)
    showServerDirs()

def deleteElements(arr):
    for i in arr:
        i.destroy()

def showServerDirs():
    global directories_el, server_dirs_el
    for k, v in server_dirs_el.items():
        deleteElements(k)
    server_dirs_el.clear()
    server_dirs = requests.get('http://127.0.0.1:5000/getDirs',
                               params={'login': main.LOGIN, 'password': '12345'}).json()
    local_dirs = [os.path.basename(x) for x in settings['directories']]
    for i, dir in enumerate(main.compareLists(local_dirs, server_dirs)['add']):
        local_lb = Label(
            frame,
            text = dir
        )
        local_lb.grid(row=i+1, column=2)

        local_btn = Button(
            frame,
            text='+',
            command=partial(createNewDir, dir),
            padx=5
        )
        local_btn.grid(row=i+1, column=3)
        server_dirs_el[dir] = [local_lb, local_btn]


def createPaths():
    global directories_el
    updateSettings()
    directories_el.clear()
    for i, path in enumerate(settings['directories']):
        local_lb = Label(
            frame,
            text = path
        )
        local_lb.grid(row=i+1, column=0)

        local_btn = Button(
            frame,
            text='X',
            command=partial(deleteDirectoryFromSettings, path),
            padx=5
        )
        local_btn.grid(row=i+1, column=1)
        directories_el[path] = [local_lb, local_btn]
    showServerDirs()
    # pprint.pprint(main.compareLists(local_dirs, server_dirs))
    return directories_el

def addDirectoryToSettings(path):
    with open(settings_path, 'r+') as f:
        data = json.load(f)
        if not path in data['directories']:
            data['directories'].append(path)  # <--- add `id` value.
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part
    MAIN_DIRECTORIES.append(path)
    th = Thread(target=start, args=(path, MAIN_DIRECTORIES))
    th.start()
    createPaths()

def chooseDir():
    file_name = tkinter.filedialog.askdirectory()
    addDirectoryToSettings(file_name)
    window.destroy()
    window.quit()
# addDirectoryToSettings('C:/Users/zubko/Desktop/insideFolderForConnection/excel')

height_lb = Label(
    frame,
    text="Login"
)
height_lb.grid(row=0, column=0)
# height_lb.place(relx=0, rely=0)

height_tf = Entry(
    frame, #Используем нашу заготовку с настроенными отступами.
)
height_tf.grid(row=0, column=1)
height_tf.insert(0, settings['login'] if settings['login'] != None else '')

cal_btn = Button(
    frame,
    text='Новый логин',
    command=edit_login,
    padx=10
)
cal_btn.grid(row=0, column=2)

choose_btn = Button(
    frame,
    text='Выбрать папку',
    command=chooseDir,
    padx=10
)
choose_btn.grid(row=0, column=3)

if main.LOGIN != None:
    createPaths()

# threads = {}
# def threads_controller(threads):
#     while True:
#         updateSettings()
#         for k, v in threads.items():
#             if k not in settings['directories']:
#                 v.

def on_close():
    global MAIN_DIRECTORIES
    MAIN_DIRECTORIES.clear()
    window.destroy()
    print('END')

window.protocol("WM_DELETE_WINDOW", on_close)

window.mainloop()


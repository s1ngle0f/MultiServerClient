import os
import sys
import json
from tkinter import *
import requests
import main
from functools import partial


settings_path = os.path.dirname(__file__) + '/settings.json'

base_path = os.getcwd().replace('\\', '/').replace('//', '/')
# base_path = 'C:/Users/zubko/Desktop/'

with open(settings_path, 'r') as f:
    data = json.load(f)

def add_path_to_settings(path):
    global data
    with open(settings_path, 'r+') as f:
        data = json.load(f)
        if not path in data['directories']:
            data['directories'].append(path)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

window = Tk()
window.title('Get folder from server')
window.geometry('150x150')

frame = Frame(
    window, #Обязательный параметр, который указывает окно для размещения Frame.
    padx = 10, #Задаём отступ по горизонтали.
    pady = 10 #Задаём отступ по вертикали.
)
frame.pack(expand=True)

def selectFolder(dir):
    os.makedirs(base_path + '/' + dir)
    add_path_to_settings(base_path + '/' + dir)

def showServerDirs():
    global directories_el, server_dirs_el, data
    server_dirs = requests.get('http://127.0.0.1:5000/getDirs',
                               params={'login': data['login'], 'password': '12345'}).json()
    local_dirs = [os.path.basename(x) for x in data['directories']]
    for i, dir in enumerate(main.compareLists(local_dirs, server_dirs)['add']):
        local_lb = Label(
            frame,
            text = dir
        )
        local_lb.grid(row=i, column=0)

        local_btn = Button(
            frame,
            text='+',
            command=partial(selectFolder, dir),
            padx=5
        )
        local_btn.grid(row=i, column=1)

showServerDirs()

window.mainloop()
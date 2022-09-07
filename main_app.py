import tkinter.filedialog
from tkinter import *
import os
import json
import run_new
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageTk
from threading import Thread
import context_menu

context_menu.create_registers()

settings_path = os.path.dirname(__file__) + '/settings.json'
window = Tk()
window.title('MultiFolder')
window.geometry('300x100')

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
        data['directories'] = []
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part
        if not run_new.IS_WORK:
            run_new.run()

def updateSettings():
    global settings
    if not os.path.exists(settings_path):
        with open(settings_path, 'w', encoding='utf-8') as f:
            data = {'login': None, 'directories': []}
            json.dump(data, f, ensure_ascii=False, indent=4)
            settings = data
    else:
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
            # print(settings)
updateSettings()

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
    text='Изменить логин',
    command=edit_login,
    padx=10
)
cal_btn.grid(row=0, column=2)

# Define a function for quit the window
def quit_window(icon, item):
   icon.stop()
   window.destroy()

# Define a function to show the window again
def show_window(icon, item):
   icon.stop()
   window.after(0, window.deiconify)

# Hide the window and show on the system taskbar
def hide_window():
   window.withdraw()
   image=Image.open('dolphin.ico')
   menu=(item('Quit', quit_window), item('Show', show_window))
   icon=pystray.Icon("name", image, "My System Tray Icon", menu)
   icon.run()

window.protocol("WM_DELETE_WINDOW", hide_window)


th = Thread(target=run_new.run)
th.start()


window.mainloop()
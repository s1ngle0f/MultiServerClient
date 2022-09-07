import winreg as reg
import os
import sys

def add_current_folder():
    key_path = r'Directory\\Background\\shell\\AddCurrentFolder'
    try:
        conn = reg.ConnectRegistry(None, reg.HKEY_LOCAL_MACHINE)
        k = reg.OpenKey(conn, key_path)
        k.Close()
    except:
        key = reg.CreateKeyEx(reg.HKEY_CLASSES_ROOT, key_path)
        reg.SetValue(key, '', reg.REG_SZ, 'Add Current Folder')
        key_command = reg.CreateKeyEx(key, r'command')
        reg.SetValue(key_command, '', reg.REG_SZ, sys.executable + ' ' + os.path.dirname(__file__) + '\\add_dir.py') #не для билда
# add_current_folder()

def delete_current_folder():
    key_path = r'Directory\\Background\\shell\\DeleteCurrentFolder'
    try:
        conn = reg.ConnectRegistry(None, reg.HKEY_LOCAL_MACHINE)
        k = reg.OpenKey(conn, key_path)
        k.Close()
    except:
        key = reg.CreateKeyEx(reg.HKEY_CLASSES_ROOT, key_path)
        reg.SetValue(key, '', reg.REG_SZ, 'Delete Current Folder')
        key_command = reg.CreateKeyEx(key, r'command')
        reg.SetValue(key_command, '', reg.REG_SZ, sys.executable + ' ' + os.path.dirname(__file__) + '\\delete_dir.py') #не для билда
# delete_current_folder()

def get_folder_from_server():
    key_path = r'Directory\\Background\\shell\\GetFolder'
    try:
        conn = reg.ConnectRegistry(None, reg.HKEY_LOCAL_MACHINE)
        k = reg.OpenKey(conn, key_path)
        k.Close()
    except:
        key = reg.CreateKeyEx(reg.HKEY_CLASSES_ROOT, key_path)
        reg.SetValue(key, '', reg.REG_SZ, 'Get Folder From Server')
        key_command = reg.CreateKeyEx(key, r'command')
        reg.SetValue(key_command, '', reg.REG_SZ, sys.executable + ' ' + os.path.dirname(__file__) + '\\get_folder_from_server.py') #не для билда
# get_folder_from_server()

def create_registers():
    add_current_folder()
    delete_current_folder()
    get_folder_from_server()
create_registers()
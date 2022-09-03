import winreg as reg
import os
import sys

def add_current_folder():
    key_path = r'Directory\\Background\\shell\\AddCurrentFolder'
    key = reg.CreateKeyEx(reg.HKEY_CLASSES_ROOT, key_path)
    reg.SetValue(key, '', reg.REG_SZ, 'Add Current Folder')
    key_command = reg.CreateKeyEx(key, r'command')
    reg.SetValue(key_command, '', reg.REG_SZ, sys.executable + ' ' + os.path.dirname(__file__) + '\\add_dir.py')
# add_current_folder()

def delete_current_folder():
    key_path = r'Directory\\Background\\shell\\DeleteCurrentFolder'
    key = reg.CreateKeyEx(reg.HKEY_CLASSES_ROOT, key_path)
    reg.SetValue(key, '', reg.REG_SZ, 'Delete Current Folder')
    key_command = reg.CreateKeyEx(key, r'command')
    reg.SetValue(key_command, '', reg.REG_SZ, sys.executable + ' ' + os.path.dirname(__file__) + '\\delete_dir.py')
# delete_current_folder()

def get_folder_from_server():
    key_path = r'Directory\\Background\\shell\\GetFolder'
    key = reg.CreateKeyEx(reg.HKEY_CLASSES_ROOT, key_path)
    reg.SetValue(key, '', reg.REG_SZ, 'Get Folder From Server')
    key_command = reg.CreateKeyEx(key, r'command')
    reg.SetValue(key_command, '', reg.REG_SZ, sys.executable + ' ' + os.path.dirname(__file__) + '\\get_folder_from_server.py')
# get_folder_from_server()
import os
import json
from main import compareLists
from time import sleep
from threading import Thread
from main import start


WORK = True
time_update = 3

def run():
    settings_path = os.getenv('APPDATA') + '/MultiFolder/settings.json'
    last_data = None
    with open(settings_path, 'r') as f:
        data = json.load(f)
    for dir in data['directories']:
        th = Thread(target=start, args=(dir,))
        th.start()
    while WORK:
        with open(settings_path, 'r') as f:
            data = json.load(f)
        if last_data is not None:
            result = compareLists(last_data['directories'], data['directories'])
            if len(result['add']) > 0:
                for path in result['add']:
                    th = Thread(target=start, args=(path, ))
                    th.start()
        last_data = data
        sleep(time_update)
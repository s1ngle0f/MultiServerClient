import os
import json
from main import compareLists
from time import sleep
from threading import Thread
from main import start


WORK = True
time_update = 3

def run():
    settings_path = os.path.dirname(__file__) + '/settings.json'
    last_data = None
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
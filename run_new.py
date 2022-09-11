import observer
import json
import os

settings_path = os.getenv('APPDATA') + '/MultiFolder/settings.json'

IS_WORK = False

def checkExisting():
    with open(settings_path, 'r') as f:
        data = json.load(f)

    for dir in data['directories']:
        if not os.path.exists(dir):
            data['directories'].remove(dir)

    with open(settings_path, 'r+') as f:
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


def run():
    global IS_WORK
    if not os.path.exists(settings_path):
        with open(settings_path, 'w', encoding='utf-8') as f:
            data = {'login': None, 'directories': []}
            json.dump(data, f, ensure_ascii=False, indent=4)
    with open(settings_path, 'r') as f:
        data = json.load(f)
    if data['login'] != None and data['login'] != '':
        IS_WORK = True
        checkExisting()
        observer.run()

# run()
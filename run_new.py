import observer
import json
import os

def checkExisting():
    settings_path = os.path.dirname(__file__) + '/settings.json'

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
    checkExisting()
    observer.run()

# run()
import os
import sys
import json

settings_path = os.path.dirname(__file__) + '/settings.json'

path = os.getcwd().replace('\\', '/').replace('//', '/')

with open(settings_path, 'r+') as f:
    data = json.load(f)
    if path in data['directories']:
        data['directories'].remove(path)
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()
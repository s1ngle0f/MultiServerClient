from threading import Thread
from main import start

folders = [
    'C:/Users/zubko/Desktop/docx',
    'C:/Users/zubko/Desktop/pwpt'
]

for i in folders:
    th = Thread(target=start, args=(i,))
    th.start()
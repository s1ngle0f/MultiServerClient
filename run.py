from threading import Thread

import main
from main import start

folders = [
    'C:/Users/zubko/Desktop/docx',
    'C:/Users/zubko/Desktop/insideFolderForConnection/excel',
    'C:/Users/zubko/Desktop/pwpt'
]

main.LOGIN = 'zubkova'

for i in folders:
    th = Thread(target=start, args=(i,))
    th.start()
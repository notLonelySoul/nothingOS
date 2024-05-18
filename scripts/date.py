from datetime import datetime
from time import localtime, strftime

info = datetime.now().strftime(r'%d,%b,%Y,')

print(info)

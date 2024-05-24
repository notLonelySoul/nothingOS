import urllib.request, json
import os

from usr_data import *

APP_ID_FILE = f"{DATA_DIR}/wolf_appid.txt"
if not os.path.isfile(APP_ID_FILE): os.mknod(APP_ID_FILE)
with open(APP_ID_FILE, 'r') as f: APP_ID = f.read().strip()

inp = input("Enter query: ").replace(' ', '%20')

query = f"http://api.wolframalpha.com/v2/query?appid={APP_ID}&input={inp}&format=image,plaintext&output=json"

with urllib.request.urlopen(query) as api_call:
    q_result = json.load(api_call)
    result = q_result['queryresult']

if result['success']: print(result['pods'][0]['subpods'])

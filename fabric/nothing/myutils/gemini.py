import google.generativeai as genai
import os
import asyncio

from usr_data import *

APP_ID_FILE = f"{DATA_DIR}/gemini_id.txt"
if not os.path.isfile(APP_ID_FILE): os.mknod(APP_ID_FILE)
with open(APP_ID_FILE, 'r') as f: KEY = f.read().strip()

genai.configure(api_key=KEY)
model = genai.GenerativeModel('gemini-pro')

results = asyncio.run(model.generate_content_async("What is life ?"))
print("hello wassup ?")
print(results.text)

import json
from src.sync_volumes import sync
download_progress='100%'
model ='1235'

with open('src/data/pull_data.json','r') as f:
    pull_data = json.load(f)
try:
    m = pull_data['model']
except:
    m = 0

if download_progress=='100%' and m == 0:
    ready = sync()
    pull_data[model] = 1
    ready = True
    with open('src/data/pull_data.json','w') as f:
        f.write(json.dumps(pull_data))
else:
    ready = False
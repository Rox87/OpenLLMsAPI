import json
from src.sync_volumes import sync
download_progress='100%'
model ='1235'
pull_data = {}
pull_data = '{}'

with open('src/data/pull_data.json','r') as f:
    pull_data = json.load(f)
    retry=5
    while len(pull_data) < 2 and retry > 0:
        retry-=1
        with open('src/data/pull_data.json','r') as f:
            pull_data = json.load(f)

print(pull_data)
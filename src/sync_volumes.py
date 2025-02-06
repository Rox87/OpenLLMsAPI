import os

async def sync():
    os.system('mkdir ~/models')
    os.system('rsync -av --delete ~/.ollama/models ~/models')
    return 'ready'
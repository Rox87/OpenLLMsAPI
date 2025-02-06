import os

def sync():
    return 'ready'
    os.system('mkdir ~/models')
    os.system('rsync -av --delete ~/.ollama/models ~/models')
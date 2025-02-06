import re

def remove_inside_tag(btag,ltag,text):
    # Use regex to remove content between <think> and </think> tags
    return re.sub(rf'{btag}.*?{ltag}', '', text)

def rm_first_line(log):
    # Dividindo o texto em linhas
    lines = log.splitlines()

    # Reconstituindo o texto sem a primeira linha
    log = "\n".join(lines[1:])
    return log

def calcular_media(lista):
    return sum(lista) / len(lista) if lista else 0

def float_para_porcentagem(valor):
    return f"{valor * 100:.0f}%"
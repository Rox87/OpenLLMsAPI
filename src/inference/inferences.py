import ollama
import time
import subprocess
from auxiliar import calcular_media, float_para_porcentagem
import json

async def data_wait(prompt, model):
    try:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": f"{prompt}"}])
    except Exception as e:
        print(f"Erro ao chamar o modelo: {e}")
        response = None
    return response


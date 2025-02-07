from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from stream import data_streamer, pull_model_stream, list_model_stream
from inference.inferences import data_wait
from models import RequestBody
import subprocess
import time
import configparser

# Criando um arquivo de configuração
config = configparser.ConfigParser()

config.read('src/config.ini',encoding='utf-8')

app = FastAPI()

@app.post('/inference')
async def inference(req:RequestBody):
    print('waitable inference start')
    prompt = f"{config['Prompts']['prepare_prompt']} {req.prompt}"
    print(f"model:{req.model}")
    print(f"prompt:{prompt}")
    return await data_wait(prompt=prompt,model=req.model)

@app.post('/stream')
async def stream(req:RequestBody):
    print('stream start')
    prompt = f"{config['Prompts']['prepare_prompt']} {req.prompt}"
    print(f"model:{req.model}")
    print(f"prompt:{prompt}")
    return StreamingResponse(data_streamer(prompt=prompt,model=req.model), media_type='text/event-stream')

@app.post("/download/{model}")
async def download(model: str):
    print('download start')
    print(f"model:{model}")
    return await pull_model_stream(model)

@app.post("/list")
async def list_models():
    print('list models start')
    return await list_model_stream()

executando = False  # Controle de execução

@app.get("/force_sync")
async def force_sync():
    global executando
    if executando:
        return {"message": "Já existe um processo de syncronização em execução. Ignorando chamada."}
    
    executando = True
    
    try:
        print("Executando processo...")
        process = subprocess.Popen(
            ['./src/sync_volumes.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Captura stdout e stderr juntos
            text=True,
            bufsize=1,  # Linha a linha
            universal_newlines=True,
            encoding="utf-8",  # Define a codificação UTF-8
            errors="ignore"  # Ignora caracteres que não podem ser decodificados
        )
        log = ""
        
        # Aguarda o tempo limite sem matar o processo
        start_time = time.time()
        while time.time() - start_time < 1:
            # Captura a saída em tempo real
            output = process.stdout.read()
            if output == '' and process.poll() is not None:
                break
            if output:
                log += output  # Adiciona a linha à variável log
        print("Processo de syncronização em execução ou finalizado.")

        return log
    
    finally:
        executando = False  # Libera para novas execuções

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
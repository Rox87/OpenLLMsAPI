import ollama
import time
import subprocess
from auxiliar import calcular_media, float_para_porcentagem


async def data_streamer(prompt, model):
    try:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": f"{prompt}"}], stream=True)
    except Exception as e:
        print(f"Erro ao chamar o modelo: {e}")
        response = None
    if response:
        for chunk in response:
            yield chunk['message']['content']
    else:
        yield "Erro ao obter resposta do modelo."

async def pull_model_stream(model):
        process = subprocess.Popen(
            ['ollama','pull',model],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Captura stdout e stderr juntos
            text=True,
            bufsize=1,  # Linha a linha
            universal_newlines=True,
            encoding="utf-8",  # Define a codificação UTF-8
            errors="ignore"  # Ignora caracteres que não podem ser decodificados
        )
        
        log = ""
        try:
            # Aguarda o tempo limite sem matar o processo
            start_time = time.time()
            while time.time() - start_time < 1:
                # Captura a saída em tempo real
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    log += output  # Adiciona a linha à variável log

           
            h=0
            p_list = []
            for line in log.splitlines():  # Divide a saída em linhas
                if h<=0:
                    line.split()
                    h+=1
                else:
                    try:
                        p_list.append(float(line.split()[2].strip('%')) / 100)
                    except:
                        pass

            download_progress = float_para_porcentagem(calcular_media(p_list))

            ready = False
            if download_progress=='100%':
                ready = True

            print(f"download_progress:{download_progress}")
                
            return {"model":model,"download_progress":download_progress, "ready": ready}
            


        except Exception as e:
            print(f"Erro inesperado: {e}")
            return None
        
async def list_model_stream():
        process = subprocess.Popen(
        ['ollama', 'list'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # Captura stdout e stderr juntos
        text=True,
        encoding="utf-8",  # Define a codificação UTF-8
        errors="ignore"  # Ignora caracteres que não podem ser decodificados
    )

        log, _ = process.communicate()  # Captura toda a saída e espera o processo terminar
        h = 0
        models_list = []
        for line in log.splitlines():  # Divide a saída em linhas
            if h<=1:
                line.split()
                h+=1
            else:
                models_list.append(line.split()[0])
        return {"models":models_list}

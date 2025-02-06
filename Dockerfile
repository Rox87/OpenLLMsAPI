FROM python:slim-bookworm
 
WORKDIR /home/dataocean
 
RUN apt update && apt install -y curl rsync
#netcat-traditional

COPY install.sh .
 
RUN chmod +x install.sh && \
    ./install.sh
 
### Install models here ###
# RUN ollama serve & \
#     while ! nc -z localhost 11434; do sleep 1; done && \
#     ollama pull qwen2.5:0.5b
 
COPY ./src ./src
 
RUN pip install --no-cache-dir -r ./src/requirements.txt
 
EXPOSE 8000
 
# Comando de inicialização do container:
# 1. inicia o script de syncronização do drive
# 2. Inicia o servidor Ollama em segundo plano
# 3. Executa o serviço FastAPI definido no arquivo `ollama.fastapi.stream.py`
CMD ["sh", "-c","./src/sync_volumes.sh & ollama serve & python src/main.py"]
# Usa a imagem oficial do Python baseada no Debian Bookworm, mas com uma versão "slim" para reduzir o tamanho.
FROM python:slim-bookworm 

# Define o diretório de trabalho dentro do container como /home/ubuntu
WORKDIR /home/dataocean

# Atualiza os pacotes do sistema e instala o curl e netcat-traditional
RUN apt update && apt install -y curl netcat-traditional rsync

# Copia o script de instalação para o container
COPY install.sh .

# Concede permissão de execução ao script e o executa
RUN chmod +x install.sh && \
    ./install.sh

# Inicia o servidor Ollama em segundo plano e aguarda ele ficar disponível na porta 11434,
# depois faz o pull do modelo `deepseek-r1:1.5b`

### Install models here ###

# RUN ollama serve & \
#     while ! nc -z localhost 11434; do sleep 1; done && \
#     ollama pull qwen2.5:0.5b

# Copia o diretório `src` para o container
COPY ./src ./src

RUN 

# Instala as dependências do projeto usando o arquivo requirements.txt, evitando o uso de cache
RUN pip install --no-cache-dir -r ./src/requirements.txt

# Expõe a porta 8000 para que o serviço possa ser acessado externamente
EXPOSE 8000

# Comando de inicialização do container:
# 1. Inicia o servidor Ollama em segundo plano
# 2. Executa o serviço FastAPI definido no arquivo `ollama.fastapi.stream.py`
CMD ["sh", "-c","./src/sync_volumes.sh & ollama serve & python src/main.py"]
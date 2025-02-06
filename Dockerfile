# Usa a imagem base do Python (versão Slim baseada no Debian Bookworm) para um ambiente mais leve
FROM python:slim-bookworm

# Define o diretório de trabalho dentro do container
WORKDIR /home/dataocean

# Atualiza os pacotes e instala dependências essenciais:
# - curl: Para baixar arquivos via HTTP/HTTPS
# - rsync: Para sincronizar arquivos e diretórios
RUN apt update && apt install -y curl rsync

# Tenta instalar o pacote nvidia-cuda-toolkit. Continua se a instalação falhar
# remover || true (em produção)
RUN apt install -y nvidia-cuda-toolkit || true

# Copia o script de instalação do Ollama para dentro do container
COPY ollama_install.sh .

# Dá permissão de execução ao script e executa a instalação do Ollama
RUN chmod +x ollama_install.sh && \
    ./ollama_install.sh

# Copia o diretório `src` da máquina local para dentro do container
COPY ./src ./src

# Instala as dependências do Python listadas em `requirements.txt`, sem armazenar cache para economizar espaço
RUN pip install --no-cache-dir -r ./src/requirements.txt

# Expõe a porta 8000 para comunicação externa (provavelmente usada pelo FastAPI)
EXPOSE 8000

# Configura as variáveis de ambiente para a aceleração por GPU no Ollama
ENV OLLAMA_ACCELERATE=cuda
# Define quais GPUs estão visíveis para o container (neste caso, as GPUs 0, 1, 2 e 3)
ENV CUDA_VISIBLE_DEVICES=0,1,2,3
# Define o limite máximo de memória que o Ollama pode usar nas GPUs (70GB)
ENV OLLAMA_MAX_GPU_MEMORY=70GB

# Comando de inicialização do container:
# 1. Executa o script `sync_volumes.sh` em segundo plano para sincronização de volumes
# 2. Inicia o servidor Ollama em segundo plano
# 3. Executa a aplicação FastAPI definida no arquivo `src/main.py`
CMD ["sh", "-c", "./src/sync_volumes.sh & ollama serve & python src/main.py"]
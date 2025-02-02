# Use Ubuntu as base image
FROM ubuntu:latest

WORKDIR /home/ubuntu
# Install dependencies
RUN apt update && apt install -y curl

RUN curl -fsSL https://ollama.com/install.sh -o install.sh

# Dê permissão de execução ao script
RUN chmod +x install.sh

# Execute o script de instalação
RUN ./install.sh

RUN ollama serve & \
    sleep 5 && \
    ollama pull deepseek-r1:8B

# Expose the API port (7860 for HF Spaces)
EXPOSE 7860

# Start Ollama on port 7860
CMD ["ollama", "serve", "--port", "7860"]
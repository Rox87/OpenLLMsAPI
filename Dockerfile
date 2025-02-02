# Use Ubuntu as base image
FROM alpine:latest

# Install dependencies
RUN apk update 

RUN apk add --no-cache curl

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Expose Ollama's API port
EXPOSE 11434

RUN ollama serve & sleep 5 && ollama pull deepseek-r1:8b
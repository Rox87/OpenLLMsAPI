# Use Ubuntu as base image
FROM ubuntu:latest

# Install dependencies
RUN apt update && apt install -y curl

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Download the model (e.g., Mistral)
RUN ollama pull mistral

# Expose Ollama's API port
EXPOSE 11434

# Start Ollama
CMD ["ollama", "serve"]
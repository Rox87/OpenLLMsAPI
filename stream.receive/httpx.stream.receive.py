import httpx
import argparse

# Create the parser
parser = argparse.ArgumentParser(description="A simple argparse example")

# Add arguments
parser.add_argument("model", type=str, help="ollama model identifier")
parser.add_argument("prompt", type=str, help="Command")

# Parse the arguments
args = parser.parse_args()

url = f"http://localhost:8000/stream"

with httpx.stream("POST",url=url,timeout=21000,json={"prompt":args.prompt,"model":args.model}) as response:
    for chunk in response.iter_text():
        print(chunk,end="",flush=True)
        
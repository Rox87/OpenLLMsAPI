from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from stream import data_streamer, pull_model_stream, list_model_stream
from inference.inferences import data_wait
from models import RequestBody
from myvars.prompts import prepare

app = FastAPI()

@app.post('/inference')
async def inference(req:RequestBody):
    print('waitable inference start')
    prompt = f"{prepare} {req.prompt}"
    print(f"model:{req.model}")
    print(f"prompt:{prompt}")
    return await data_wait(prompt=prompt,model=req.model)

@app.post('/stream')
async def stream(req:RequestBody):
    print('stream start')
    prompt = f"{prepare} {req.prompt}"
    print(f"model:{req.model}")
    print(f"prompt:{prompt}")
    return StreamingResponse(data_streamer(prompt=prompt,model=req.model), media_type='text/event-stream')

@app.post("/download/{model}")
async def download(model: str):
    print('download start')
    print(f"model:{model}")
    return StreamingResponse(await pull_model_stream(model), media_type='text/event-stream')

@app.post("/list")
async def list_models():
    print('list models start')
    return StreamingResponse(await list_model_stream(), media_type='text/event-stream')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
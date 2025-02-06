from pydantic import BaseModel

class RequestBody(BaseModel):
    prompt: str
    model: str
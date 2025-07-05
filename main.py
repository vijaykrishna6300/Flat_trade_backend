from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class LoginData(BaseModel):
    client_code: str
    password: str
    totp_secret: str
    api_key: str

@app.post("/login")
async def login(data: LoginData):
    return {"message": "Data received", "data": data}

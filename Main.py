from fastapi import FastAPI
from pydantic import BaseModel
import pyotp
import requests

app = FastAPI()

class LoginRequest(BaseModel):
    client_code: str
    password: str
    totp_secret: str
    api_key: str

@app.post("/login")
def login(data: LoginRequest):
    totp = pyotp.TOTP(data.totp_secret).now()

    payload = {
        "clientCode": data.client_code,
        "password": data.password,
        "totp": totp
    }

    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": data.api_key
    }

    response = requests.post("https://authapi.flattrade.in/trade/authenticate",
                             json=payload, headers=headers)

    return response.json()

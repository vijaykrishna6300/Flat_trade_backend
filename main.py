from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
import pyotp

app = FastAPI()

class LoginData(BaseModel):
    client_code: str
    password: str
    totp_secret: str
    api_key: str

@app.post("/login")
async def login(data: LoginData):
    # Generate TOTP using secret
    totp = pyotp.TOTP(data.totp_secret).now()

    # Prepare request to Flattrade API
    payload = {
        "clientCode": data.client_code,
        "password": data.password,
        "totp": totp
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-API-KEY": data.api_key
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://auth.flattrade.in/api/login",
                json=payload,
                headers=headers
            )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

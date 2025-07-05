from fastapi import FastAPI, HTTPException
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
    try:
        # 1. Generate TOTP
        totp = pyotp.TOTP(data.totp_secret)
        otp = totp.now()

        # 2. Prepare login payload
        payload = {
            "client_code": data.client_code,
            "password": data.password,
            "totp": otp
        }

        # 3. Call Flattrade login API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://authapi.flattrade.in/trade/apitoken",
                headers={"Content-Type": "application/json", "X-API-KEY": data.api_key},
                json=payload
            )

        # 4. Return Flattrade response
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=400, detail=response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

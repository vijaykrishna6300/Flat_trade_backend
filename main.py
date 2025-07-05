from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import traceback

app = FastAPI()

class LoginRequest(BaseModel):
    client_code: str
    password: str
    totp_secret: str
    api_key: str

@app.post("/login")
def login(data: LoginRequest):
    try:
        # 🔒 Your Flattrade login logic goes here
        # For now just return dummy success
        return {"message": "Login successful"}
    
    except Exception as e:
        print("ERROR OCCURRED:\n", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

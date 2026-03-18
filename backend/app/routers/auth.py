import bcrypt

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.config import settings
from app.utils.auth import create_token

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    username: str


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest):
    password_ok = bcrypt.checkpw(body.password.encode(), settings.ADMIN_PASSWORD_HASH.encode())
    if body.username != settings.ADMIN_USERNAME or not password_ok:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = create_token(body.username)
    return LoginResponse(token=token, username=body.username)

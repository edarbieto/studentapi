from fastapi import APIRouter, Depends, Response
import src.features.auth.model as auth_model
import src.features.auth.service as auth_service
from src.features.auth.dependency import getcurrentuser
from src.config import settings
import sqlite3

router = APIRouter(prefix="/auth", tags=["/auth"])

@router.post("/login")
def login(logindata: auth_model.LoginData, response: Response):
    with sqlite3.connect(settings.DB_URI) as conn:
        token = auth_service.login(conn,
                                   logindata.email,
                                   logindata.password)
    response.set_cookie("accesstoken", token, httponly=True)
    return {"accesstoken": token}

@router.post("/register")
def register(registerdata: auth_model.RegisterData):
    with sqlite3.connect(settings.DB_URI) as conn:
        msg = auth_service.register(conn,
                                    registerdata.email,
                                    registerdata.password,
                                    registerdata.firstname,
                                    registerdata.lastname,
                                    registerdata.phone)
        conn.commit()
    return {"msg": msg}

@router.get("/me")
def me(loginuser: auth_model.LoginUser = Depends(getcurrentuser())):
    return loginuser
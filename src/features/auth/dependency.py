from fastapi import Cookie, HTTPException
from typing import Annotated
from src.features.auth.model import LoginUser
from src.config import settings
from jose import jwt

def getcurrentuser(required: bool = True):
    def _gettoken(accesstoken: Annotated[str, Cookie()] = None):
        if not required and not accesstoken:
            return None
        try:
            if not accesstoken:
                raise Exception("Login required")
            obj = jwt.decode(accesstoken, settings.JWT_SECRET)
            loginuser = LoginUser(
                id=obj["id"],
                email=obj["email"],
                firstname=obj["firstname"],
                lastname=obj["lastname"],
                phone=obj["phone"],
            )
            return loginuser
        except Exception as e:
            print(str(e))
            raise HTTPException(
                status_code=401,
                detail="Login required",
            )
    return _gettoken
from pydantic import BaseModel

class LoginData(BaseModel):
    email: str
    password: str

class RegisterData(BaseModel):
    email: str
    password: str
    firstname: str
    lastname: str
    phone: str | None = None

class LoginUser(BaseModel):
    id: int
    email: str
    firstname: str
    lastname: str
    phone: str | None = None
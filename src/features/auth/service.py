from sqlite3 import Connection
from src.config import salt, settings
from fastapi import HTTPException
from jose import jwt
import bcrypt

def login(conn: Connection, email: str, password: str):
    cur = conn.cursor()
    query = f"""
        select
            id,
            password,
            firstname,
            lastname,
            phone
        from users
        where email = ?
    """
    params = [email]
    cur.execute(query, params)
    rs = cur.fetchall()
    if len(rs) != 1:
        raise HTTPException(
            status_code=400,
            detail="Email does not exist",
        )
    id = rs[0][0]
    hashedpassword = rs[0][1]
    firstname = rs[0][2]
    lastname = rs[0][3]
    phone = rs[0][4]
    matchpassword = bcrypt.checkpw(password.encode(), hashedpassword.encode())
    if not matchpassword:
        raise HTTPException(
            status_code=400,
            detail="Incorrect password",
        )
    obj = {
        "id": id,
        "email": email,
        "firstname": firstname,
        "lastname": lastname,
        "phone": phone,
    }
    token = jwt.encode(obj, settings.JWT_SECRET)
    return token

def register(conn: Connection, email: str, password: str, firstname: str, lastname: str, phone: str):
    cur = conn.cursor()
    hashedpassword = bcrypt.hashpw(password.encode(), salt).decode()
    query = f"""
        insert into users (email, password, firstname, lastname, phone)
        values (?, ?, ?, ?, ?)
    """
    params = [email, hashedpassword, firstname, lastname, phone]
    cur.execute(query, params)
    msg = "Register successful"
    return msg
from jose import jwt, JWTError
from datetime import datetime,timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from fastapi import  Depends,Response,status,HTTPException
from .config import settings

oath2_schemas = OAuth2PasswordBearer(tokenUrl="/login")


#secret key
#algorith
#expiration time

SECRET_KEY = settings.secret_key
#secret key is any string

ALGORITH = settings.algorith
ACCESS_TOLEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_acess_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOLEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITH)
    
    return encoded_jwt

def verify_acess_token(token:str,credential_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms= [ALGORITH] )
        id = int(payload.get("user_id"))

        if not id:
            raise credential_exception
        
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credential_exception
    
    return token_data

def get_current_user(token:str = Depends(oath2_schemas)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid credentials" , headers={"WWW-Authentication":"bearer"})

    return verify_acess_token(token,credential_exception)
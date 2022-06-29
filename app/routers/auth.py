from fastapi import  Depends,status,HTTPException,APIRouter
from sqlalchemy.orm import Session
from .. import models,auth2,schemas
from ..database import   get_db
from ..utils import validate
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/login",tags=["authentication"]
)

@router.post("/",response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db :Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"incorrect credentials")
    
    if not validate(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"incorrect credentials")

    acess_token = auth2.create_acess_token(data = {"user_id":user.id})
    return {"acess_token":acess_token,
            "token_type":"bearer"}
    
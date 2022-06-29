from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr, conint

class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True

class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id:int
    email:EmailStr
    class Config:
        orm_mode = True
#now this scheme is defined for the data we recieve from database through api and specify which fiel we want to show to user
class Post(BaseModel):  
    id:int
    title:str
    created_at:datetime
    owner_id:int
    owner:UserOut
    
    #this tells pydantic that vale returned is not in form of dict but on orm model , contert it to dict
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post:Post
    votes:int
#for users

class CreateUser(BaseModel):
    email:EmailStr
    password:str

# class UserOut(BaseModel):
#     id:int
#     email:EmailStr
#     class Config:
#         orm_mode = True

class Token(BaseModel):
    acess_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]=None

class Vote(BaseModel):
    post_id:int
    vote_dir:conint(le=1)
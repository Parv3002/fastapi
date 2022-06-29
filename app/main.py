# from multiprocessing import synchronize
# from pyexpat import model
# from turtle import title
# from typing import Optional,List
from .database import  engine, get_db
# from fastapi import  Depends, FastAPI,Response,status,HTTPException
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# from sqlalchemy.orm import Session
from . import models,schemas,utils

from .routers import post,user,auth,vote



models.Base.metadata.create_all(bind = engine)

app = FastAPI()
origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",

    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return{"message":"hello world"}







































# import psycopg2
# import time
# from psycopg2.extras import RealDictCursor
# class Post(BaseModel):
#     title : str
#     content : str
#     published:bool= True
    

# while True:
#     try:
#         conn = psycopg2.connect(host = "localhost",
#                                 database = "fastapi",
#                                 user = "postgres",
#                                 password = "Parvjainp12",
#                                 cursor_factory = RealDictCursor)

#         cursor = conn.cursor()
#         print("data base connection was successfull")
#         break
#     except Exception as error:
#         print("connection to database failed")
#         print("error: ",error)
#         time.sleep(2)








































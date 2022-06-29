from typing import List, Optional
from fastapi import  Depends,Response,status,HTTPException,APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models,schemas,auth2
from ..database import   get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"] # in fast api documentation for seperate tags documentations get seperated
)

@router.get("/",response_model=List[schemas.PostOut] )
def get_posts(db:Session = Depends(get_db),user_id : int = Depends(auth2.get_current_user),Limit :int = 10,skip:int = 0 ,search:Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit ).offset(skip ).all()

    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id==models.Vote.post_id,isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit ).offset(skip ).all()
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post )
def posts(post:schemas.PostCreate,db:Session = Depends(get_db),user_id : int = Depends(auth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s)  RETURNING * """,
    # (post.title,post.content,post.published))
    # post = cursor.fetchone()
    # conn.commit()
    print(user_id )
    posts = models.Post(owner_id = user_id.id, **post.dict() )
    # post = models.Post(title = post.title, content = post.content, published = post.published)
    db.add(posts)
    db.commit() # after commiting we dont have acess to post data
    db.refresh(posts) # like we say returning * it means same as refresh
    return posts


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db:Session = Depends(get_db),user_id : int = Depends(auth2.get_current_user),Limit :int = 10,skip:int = 0 ,search:Optional[str] = ""):

    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id),))
    # posts = cursor.fetchone()

    # posts = db.query(models.Post).filter(models.Post.id == id).first()
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id==models.Vote.post_id,isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit ).offset(skip ).all()
    if not posts:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post withh id {id} not found")

    return posts

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),user_id : int = Depends(auth2.get_current_user)):
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    # deleted_post =  cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id) 
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    if deleted_post.first().owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"post with id {id} is not created by you")

    deleted_post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int, post:schemas.PostCreate,db:Session = Depends(get_db),user_id : int = Depends(auth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s returning *""",(post.title,post.content,post.published,str(id)))
    # updated_post  = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    if updated_post.first().owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"post with id {id} is not created by you")
    updated_post.update(post.dict(),synchronize_session=False)
    return updated_post.first()

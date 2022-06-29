
from fastapi import  Depends,status,HTTPException,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,auth2
from ..database import   get_db

router = APIRouter(prefix="/vote",tags=["Vote"])

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session = Depends(get_db),user_id:int = Depends(auth2.get_current_user) ):

    posts = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with post id = {vote.post_id} not found ")

    vote_query = db.query(models.Vote).filter(models.Vote.user_id == user_id.id ,
    models.Vote.post_id == vote.post_id)
    vote_data = vote_query.first()
    if vote.vote_dir == 1:
        if vote_data:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user id {user_id.id} already voted post id {vote.post_id}")
        new_vote = models.Vote(user_id = user_id.id ,post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully voted"}
    else:
        if not vote_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not voted")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"vote deleted successfully"}
    

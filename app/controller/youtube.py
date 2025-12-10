from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dto.request import YoutubeInput
from app.services.youtube_service import get_youtube_comments, get_youtube_sentiment
from app.config.database import get_db

router = APIRouter(prefix="/youtube", tags=["Youtube"])

@router.post("/")
def get_comments(input: YoutubeInput):
    return get_youtube_comments(input)

@router.post("/sentiment")
def get_comment_sentiment(input: YoutubeInput, db: Session = Depends(get_db)):
    return get_youtube_sentiment(input, db)
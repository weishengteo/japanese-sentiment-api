from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dto.request import TextInput
from app.services.sentiment_service import analyze_sentiment
from app.config.database import get_db

# Declare router for sentiment
router = APIRouter(prefix="/sentiment", tags=["Sentiment"])

@router.post("/")
def sentiment(input: TextInput, db: Session = Depends(get_db)):
    return analyze_sentiment(input)
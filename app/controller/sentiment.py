from fastapi import APIRouter
from app.dto.request import TextInput
from app.services.sentiment_service import analyze_sentiment

# Declare router for sentiment
router = APIRouter(prefix="/sentiment", tags=["Sentiment"])

@router.post("/")
def sentiment(input: TextInput):
    return analyze_sentiment(input)
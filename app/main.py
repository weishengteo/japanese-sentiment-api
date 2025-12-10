from fastapi import FastAPI
from app.controller.sentiment import router as sentiment_router
from app.controller.youtube import router as youtube_router

# Fast API initialization
app = FastAPI(title = "Japanese Sentiment Analysis API")

app.include_router(sentiment_router)
app.include_router(youtube_router)
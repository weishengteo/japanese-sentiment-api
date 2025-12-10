from googleapiclient.discovery import build
from app.config.settings import settings
from app.dto.request import YoutubeInput, TextInput
from app.services.sentiment_service import analyze_sentiment
from sqlalchemy.orm import Session

youtube = build(
    "youtube",
    "v3",
    developerKey=settings.YOUTUBE_API_KEY
)

def get_youtube_comments(input: YoutubeInput):
    # Get input fields
    video_id = input.video_id
    max_comments = input.max_comments

    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=30,
        textFormat="plainText"
    )

    while request and len(comments) < max_comments:
        response = request.execute()
        for item in response["items"]:
            comments.append(
                item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            )
        request = youtube.commentThreads().list_next(request, response)

    return comments[:max_comments]

def get_youtube_sentiment(input: YoutubeInput, db: Session):
    comments = get_youtube_comments(input)

    res = []
    for comment in comments:
        sentiment = analyze_sentiment(TextInput(text = comment), db)
        res.append({
            "comment": comment,
            "sentiment": sentiment["sentiment"],
            "score": sentiment["score"]
        })
    return {"video_id": input.video_id, "comments_sentiment": res}
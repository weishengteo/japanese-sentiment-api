from googleapiclient.discovery import build
from app.config.settings import settings
from app.dto.request import YoutubeInput, TextInput
from app.services.sentiment_service import analyze_sentiment
from sqlalchemy.orm import Session
from app.models.Sentiment import Sentiment

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
    sentiment_count = {}
    records = []

    for comment in comments:
        sentiment = analyze_sentiment(TextInput(text = comment))

        label = sentiment["sentiment"].upper()
        score = sentiment["score"]

        res.append({
            "comment": comment,
            "sentiment": label,
            "score": score
        })

        # Get count
        sentiment_count[label] = sentiment_count.get(label, 0) + 1

        records.append(
            Sentiment(
                video_id=input.video_id,
                text=comment,
                sentiment=label,
                score=score
            )
        )
    
    # Bulk save to db
    save_sentiments_bulk(db, records)

    return {"video_id": input.video_id, "comments_sentiment": res, "sentiment_counts": sentiment_count}

def save_sentiments_bulk(db: Session, record: list[Sentiment]):
    try:
        db.add_all(record)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
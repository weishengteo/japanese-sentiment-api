from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from app.config.database import Base

class Sentiment(Base):
    __tablename__ = "sentiments"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, nullable=False)
    text = Column(String, nullable=False)
    sentiment = Column(String, nullable=False)
    score = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("video_id", "text", name="uq_video_text"),
    )
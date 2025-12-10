from sqlalchemy import Column, Integer, String, Float
from app.config.database import Base

class Sentiment(Base):
    __tablename__ = "sentiments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    sentiment = Column(String, nullable=False)
    score = Column(Float, nullable=False)
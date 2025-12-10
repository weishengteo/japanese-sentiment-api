from pydantic import BaseModel

class TextInput(BaseModel):
    text: str

class YoutubeInput(BaseModel):
    video_id: str
    max_comments: int = 10
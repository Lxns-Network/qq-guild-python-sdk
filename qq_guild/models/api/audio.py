from pydantic import BaseModel

class STATUS:
    START = 0
    PAUSE = 1
    RESUME = 2
    STOP = 3

class AudioAction(BaseModel):
    guild_id: str
    channel_id: str
    audio_url: str
    text: str

class AudioControl(BaseModel):
    audio_url: str
    text: str
    status: int
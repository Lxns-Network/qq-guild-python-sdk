from pydantic import BaseModel

class Announces(BaseModel):
    guild_id: str
    channel_id: str
    message_id: str
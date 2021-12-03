from enum import Enum
from pydantic import BaseModel

class Channel(BaseModel):
    id:	str
    guild_id: str
    name: str
    type: int
    sub_type: int
    position: int
    parent_id: str
    owner_id: str

class ChannelType(str, Enum):
    text = 0
    voice = 2
    live = 10005

class ChannelSubType(str, Enum):
    chat = 0
    notice = 1
    introduction = 2
    game = 3

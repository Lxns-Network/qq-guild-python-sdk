from enum import Enum
from pydantic import BaseModel
from typing import Optional

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

class PrivateType(str, Enum):
    public = 0
    admin = 1
    admin_and_member = 2

class SpeakPermission(str, Enum):
    unknown = 0
    everyone = 1
    admin_and_member = 2

class ChannelPermissions(BaseModel):
    channel_id: str
    user_id: Optional[str]
    role_id: Optional[str]
    permissions: str
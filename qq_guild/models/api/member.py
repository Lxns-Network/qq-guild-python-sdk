from typing import Optional, List
from pydantic import BaseModel
from .user import User

class Member(BaseModel):
    user: Optional[User]
    nick: Optional[str]
    roles: List[str]
    joined_at: str

class MemberWithGuildID(BaseModel):
    guild_id: str
    user: User
    nick: str
    roles: List[str]
    joined_at: str

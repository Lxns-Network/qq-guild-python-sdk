from pydantic import BaseModel, Field
from typing import Optional, List
from .user import User
from .member import Member

class MessageEmbedField(BaseModel):
    name: str 
    value: str

class MessageEmbed(BaseModel):
    title: str
    description: str
    prompt: str
    timestamp: str
    Fields: List[MessageEmbedField] = Field(..., alias="fields")

class MessageAttachment(BaseModel):
    url: str

class MessageArkObjKv(BaseModel):
    key: str
    value: str

class MessageArkObj(BaseModel):
    obj: List[MessageArkObjKv]

class MessageArk(BaseModel):
    template_id: int
    kv: List[MessageArkObj]

class Message(BaseModel):
    id: str
    channel_id: str
    guild_id: str
    content: Optional[str]
    timestamp:  str
    edited_timestamp: Optional[str]
    mention_everyone: Optional[bool]
    author: User
    attachments: Optional[List[MessageAttachment]]
    embeds: Optional[List[MessageEmbed]]

    mentions: Optional[List[User]]

    member: Optional[Member]
    ark: Optional[MessageArk]

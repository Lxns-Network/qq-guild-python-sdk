from enum import Enum
from pydantic import BaseModel

class ReactionTargetType(str, Enum):
    message = 0
    forum = 1
    comment = 2
    reply = 3

class ReactionTarget(BaseModel):
    id: str
    type: ReactionTargetType

class EmojiType(str, Enum):
    system = 1
    emoji = 2

class Emoji(BaseModel):
    id: str
    type: EmojiType

class MessageReaction(BaseModel):
    user_id: str
    guild_id: str
    channel_id: str
    target: ReactionTarget
    emoji: Emoji
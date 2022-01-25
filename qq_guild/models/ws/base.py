from typing import Optional, Union

from pydantic import BaseModel

from qq_guild.models.api.reaction import MessageReaction

from ..api import AudioAction, Channel, Guild, MemberWithGuildID, Message, MessageAudited
from .authorization import Authorization
from .ready import Ready

class HeartBeat(BaseModel):
    heartbeat_interval: int

class Load(BaseModel):
    op: int
    d: Optional[
        Union[int, str, Ready, HeartBeat, Authorization, Guild, Message, Channel, MemberWithGuildID, AudioAction, MessageAudited, MessageReaction]]
    s: Optional[int]
    t: Optional[str]

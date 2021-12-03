from typing import Optional, Union

from pydantic import BaseModel

from ..api import AudioAction, Channel, Guild, MemberWithGuildID, Message
from .authorization import Authorization
from .ready import Ready

class HeartBeat(BaseModel):
    heartbeat_interval: int

class Load(BaseModel):
    op: int
    d: Optional[
        Union[int, str, Ready, HeartBeat, Authorization, Guild, Message, Channel, MemberWithGuildID, AudioAction]]
    s: Optional[int]
    t: Optional[str]

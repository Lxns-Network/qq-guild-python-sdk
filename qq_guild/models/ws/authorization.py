from typing import Optional, List
from pydantic import BaseModel, Field

class Properties(BaseModel):
    os: int = Field(alias='$os')
    browser: str = Field(alias='$browser')
    device: str = Field(alias='$device')

class Authorization(BaseModel):
    token: str
    intents: int
    shard: List[int]
    properties: Optional[Properties]

class Resumed(BaseModel):
    token: str
    session_id: str
    seq: int

class Intents(BaseModel):
    guilds: bool
    guildMembers: bool
    directMessage: bool
    audioAction: bool
    atMessages: bool

    def __init__(self, guilds=True, guildMembers=True, directMessage=False, audioAction=True, atMessages=True):
        super().__init__(guilds=guilds, guildMembers=guildMembers, directMessage=directMessage, audioAction=audioAction, atMessages=atMessages)
    
    def to_int(self):
        return 0|self.guilds<<0 +\
               0|self.guildMembers<<1 +\
               0|self.directMessage<<12 +\
               0|self.audioAction<<29 +\
               0|self.atMessages<<30

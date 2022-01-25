from enum import Enum
from pydantic import BaseModel
from typing import Optional
from .member import Member

class Schedule(BaseModel):
    id: Optional[str]
    name: str
    description: str
    start_timestamp: str
    end_timestamp: str
    creator: Member
    jump_channel_id: str
    remind_type: str

class RemindType(str, Enum):
    no_remind = 0
    remind_when_start = 1
    remind_before_5_minutes = 2
    remind_before_15_minutes = 3
    remind_before_30_minutes = 4
    remind_before_60_minutes = 5
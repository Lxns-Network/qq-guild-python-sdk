from typing import Optional
from pydantic import BaseModel

class Guild(BaseModel):
    id: str
    name: str
    icon: Optional[str]
    owner_id: Optional[str]
    owner: Optional[bool]
    op_user_id: Optional[str]
    member_count: Optional[int]
    max_members: Optional[int]
    description: Optional[str]
    joined_at: Optional[str]
    union_world_id: Optional[str]
    union_org_id: Optional[str]

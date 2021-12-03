from pydantic import BaseModel
from typing import List

class DefaultRoles:
    all = 1
    guild_host = 2
    host = 4
    channel_admin = 5

class Role(BaseModel):
    id: str
    name: str
    color: int
    hoist: int
    number: int
    member_limit: int

class RoleRequest(BaseModel):
    guild_id: str
    roles: List[Role]
    role_num_limit: str

class RolesFilter(BaseModel):
    name: int
    color: int
    hoist: int

class RolesInfo(BaseModel):
    name: str
    color: int
    hoist: int

from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: str
    username: str
    avatar: Optional[str]
    bot: Optional[bool]
    union_openid: Optional[str]
    union_user_account: Optional[str]

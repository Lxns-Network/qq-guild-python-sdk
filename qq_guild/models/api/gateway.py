from pydantic import BaseModel

class SessionStartLimit(BaseModel):
    total: int
    remaining: int
    reset_after: int
    max_concurrency: int

class Shards(BaseModel):
    url: str
    shards: int
    session_start_limit: SessionStartLimit

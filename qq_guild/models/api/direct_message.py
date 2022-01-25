from pydantic import BaseModel

class DMS(BaseModel):
    channel_id: str
    create_time: str

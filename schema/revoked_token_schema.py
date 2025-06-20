from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RevokedTokenSchema(BaseModel):
    id: int
    token: Optional[str]
    revoked_dt: datetime

    class Config:
        from_attributes = True

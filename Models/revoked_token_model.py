from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from Database.connection import Base

class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(500), nullable=False, unique=True)
    revoked_dt = Column(DateTime, default=datetime.utcnow)

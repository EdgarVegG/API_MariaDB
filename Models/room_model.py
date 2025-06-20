from sqlalchemy import Column, Integer, String, Boolean
from Database.connection import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    ubication = Column(String(300), nullable=False)
    capacity = Column(Integer, nullable=True)
    availability = Column(Boolean, default=True)

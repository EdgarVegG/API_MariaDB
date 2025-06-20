from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    # Relación inversa con reservaciones
    reservations = relationship("Reservation", back_populates="user")


# Modelo Pydantic para exponer datos públicos sin password
class UserPublicModel(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True  # Habilita ORM mode

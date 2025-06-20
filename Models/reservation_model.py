from sqlalchemy import Column, Integer, String, Time, Date, ForeignKey
from sqlalchemy.orm import relationship
from Database.connection import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    name_event = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    select_date = Column(Date, nullable=False)
    materia = Column(String(100), nullable=True)

    # Relación con el usuario
    id_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    name_user = Column(String(100), nullable=False)

    # Relación hacia el modelo User (debe estar definido como `User`)
    user = relationship("User", back_populates="reservations")

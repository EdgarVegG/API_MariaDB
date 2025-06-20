from datetime import time, date
from pydantic import BaseModel, Field
from typing import Optional

class ReservationBase(BaseModel):
    name_event: str
    description: Optional[str] = None
    select_date: date
    start_time: time
    end_time: time
    materia: Optional[str] = None

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(BaseModel):
    name_event: Optional[str] = None
    description: Optional[str] = None
    select_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    materia: Optional[str] = None

class ReservationInDB(ReservationBase):
    id: int

    class Config:
        from_attributes = True

class ReservationResponseModel(ReservationInDB):
    # Aquí agregas solo si tu base de datos tiene o tu lógica maneja usuario
    # Si tienes usuario, deberías agregar ese campo también en el modelo SQLAlchemy
    id_user: Optional[int] = None
    name_user: Optional[str] = None
    

    class Config:
        validate_by_name = True

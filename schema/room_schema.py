from pydantic import BaseModel
from typing import Optional

# Modelo base
class RoomBase(BaseModel):
    name: str
    ubication: str
    capacity: Optional[int] = None
    availability: bool = True

# Para crear una sala
class RoomCreate(RoomBase):
    pass

# Para actualizar una sala
class RoomUpdate(BaseModel):
    name: Optional[str] = None
    ubication: Optional[str] = None
    capacity: Optional[int] = None
    availability: Optional[bool] = None

# Para respuesta completa
class RoomResponse(RoomBase):
    id: int  # corresponde al ID autoincremental de MariaDB

    class Config:
        from_attributes = True  # Necesario para mapear desde SQLAlchemy

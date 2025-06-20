from pydantic import BaseModel, EmailStr
from typing import Optional

# Modelo base para entrada (registro o actualización)
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # requerido al registrar

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

# Modelo que representa a un usuario guardado (respuesta pública)
class UserPublicModel(UserBase):
    id: int

    class Config:
        from_attributes = True

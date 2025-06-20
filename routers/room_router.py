from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import List
from sqlalchemy.orm import Session

from Database.connection import get_db
from Dependencies.dependencies import get_current_user
from schema.room_schema import RoomCreate, RoomUpdate, RoomBase
from Models.room_model import Room as RoomModel
from Models.user_model import UserPublicModel

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("/", response_model=RoomBase, status_code=status.HTTP_201_CREATED)
def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db),
    current_user: UserPublicModel = Depends(get_current_user)
):
    new_room = RoomModel(**room.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@router.get("/", response_model=List[RoomBase])
def get_rooms(db: Session = Depends(get_db)):
    rooms = db.query(RoomModel).all()
    return rooms

@router.get("/{room_id}", response_model=RoomBase)
def get_room(
    room_id: int = Path(..., description="ID de la sala"),
    db: Session = Depends(get_db)
):
    room = db.query(RoomModel).filter(RoomModel.id == room_id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala no encontrada")
    return room

@router.put("/{room_id}", response_model=RoomBase)
def update_room(
    room_id: int = Path(..., description="ID de la sala"),
    room: RoomUpdate = ...,
    db: Session = Depends(get_db),
    current_user: UserPublicModel = Depends(get_current_user)
):
    existing_room = db.query(RoomModel).filter(RoomModel.id == room_id).first()
    if not existing_room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala no encontrada")

    update_data = room.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar")

    for key, value in update_data.items():
        setattr(existing_room, key, value)

    db.commit()
    db.refresh(existing_room)
    return existing_room

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(
    room_id: int = Path(..., description="ID de la sala"),
    db: Session = Depends(get_db),
    current_user: UserPublicModel = Depends(get_current_user)
):
    room = db.query(RoomModel).filter(RoomModel.id == room_id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala no encontrada")

    db.delete(room)
    db.commit()
    return None

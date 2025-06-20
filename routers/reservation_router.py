from fastapi import APIRouter, Depends, HTTPException, status, Path
from datetime import datetime, time
from typing import List
from sqlalchemy.orm import Session

from schema.reservation_schema import ReservationCreate, ReservationUpdate, ReservationResponseModel
from Models.user_model import UserPublicModel
from Models.reservation_model import Reservation
from Database.connection import get_db
from Dependencies.dependencies import get_current_user

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post("/", response_model=ReservationResponseModel, status_code=status.HTTP_201_CREATED)
def create_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: UserPublicModel = Depends(get_current_user)
):
    start_dt = datetime.combine(reservation.select_date, reservation.start_time)
    end_dt = datetime.combine(reservation.select_date, reservation.end_time)

    if start_dt >= end_dt:
        raise HTTPException(status_code=400, detail="La hora de inicio debe ser menor que la hora de fin.")

    # Verificar traslapes en la fecha y hora
    overlapping = db.query(Reservation).filter(
        Reservation.select_date == reservation.select_date,
        Reservation.start_time < end_dt.time(),
        Reservation.end_time > start_dt.time()
    ).first()

    if overlapping:
        raise HTTPException(status_code=409, detail="Ya existe una reservación en ese horario.")

    new_reservation = Reservation(
        name_user=current_user.name,
        name_event=reservation.name_event,
        description=reservation.description,
        start_time=reservation.start_time,
        end_time=reservation.end_time,
        select_date=reservation.select_date,
        materia=reservation.materia,
        id_user=current_user.id
    )
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)

    return new_reservation

@router.get("/", response_model=List[ReservationResponseModel])
def get_reservations(db: Session = Depends(get_db)):
    reservations = db.query(Reservation).all()
    return reservations

@router.get("/{reservation_id}", response_model=ReservationResponseModel)
def get_reservation(
    reservation_id: int = Path(..., description="ID de la reservación"),
    db: Session = Depends(get_db)
):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservación no encontrada")
    return reservation

@router.put("/{reservation_id}", response_model=ReservationResponseModel)
def update_reservation(
    reservation_update: ReservationUpdate,
    reservation_id: int = Path(..., description="ID de la reservación a actualizar"),
    db: Session = Depends(get_db),
    current_user: UserPublicModel = Depends(get_current_user)
):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservación no encontrada")

    if reservation.id_user != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado para actualizar esta reservación")

    for var, value in vars(reservation_update).items():
        if value is not None:
            setattr(reservation, var, value)

    # Validar horas y fecha si se modificaron (opcional)
    if reservation.start_time >= reservation.end_time:
        raise HTTPException(status_code=400, detail="La hora de inicio debe ser menor que la hora de fin.")

    db.commit()
    db.refresh(reservation)
    return reservation

@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: UserPublicModel = Depends(get_current_user)
):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservación no encontrada")

    if reservation.id_user != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado para eliminar esta reservación")

    db.delete(reservation)
    db.commit()
    return {"message": "Reservación eliminada exitosamente"}

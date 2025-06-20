from fastapi import APIRouter, Depends, HTTPException, status, Response, Path
from sqlalchemy.orm import Session
from utils.auth_utils import hash_password
from Models.user_model import User
from schema.user_schema import UserCreate, UserUpdate, UserPublicModel
from Dependencies.dependencies import get_current_user
from Database.connection import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    hashed_pw = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuario registrado exitosamente"}

@router.get("/user/me", response_model=UserPublicModel)
def get_me(current_user: UserPublicModel = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=list[UserPublicModel])
def get_users(db: Session = Depends(get_db), current_user: UserPublicModel = Depends(get_current_user)):
    users = db.query(User).all()
    return users

@router.get("/{user_id}", response_model=UserPublicModel)
def get_user(
    user_id: int = Path(..., description="ID del usuario"),
    db: Session = Depends(get_db),
    current_user: UserPublicModel = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.put("/{user_id}", response_model=UserPublicModel)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserPublicModel = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este usuario")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    update_data = user_data.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserPublicModel = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este usuario")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

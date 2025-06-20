from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from utils.jwt_utils import verify_access_token
from Database.connection import get_db
from Models.user_model import UserPublicModel, User  # El modelo SQLAlchemy y el Pydantic
from Models.revoked_token_model import RevokedToken  # Modelo SQLAlchemy para tokens revocados

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserPublicModel:
    # 1. Verificar si el token fue revocado
    revoked = db.query(RevokedToken).filter(RevokedToken.token == token).first()
    if revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revocado. Inicia sesión nuevamente.",
        )

    # 2. Verificar validez del token
    try:
        payload = verify_access_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token sin información de usuario",
        )

    # 3. Buscar usuario en la base de datos por ID (entero)
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    # 4. Devolver un modelo público (sin contraseña)
    return UserPublicModel.from_orm(user)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from config import Settings  # importar configuración centralizada
from routers import reservation_router, room_router, user_router, auth_router

app = FastAPI(title="Api Reservation - Agenda Audiovisual")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción aquí poner los orígenes seguros
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(room_router.router)
app.include_router(reservation_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)
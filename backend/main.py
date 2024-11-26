from fastapi import FastAPI
from database import engine
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import models
from routes import (
    autenticacion,
    autores,
    categorias,
    libros,
    usuarios,
    carrito,
    pedidos,
    valoraciones,
    tarjetas,
    registros,
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware, secret_key="127a2j3k4l5k6j7h8g9f0d1s2a3d4f5g6h7j8k9l0"
)

app.include_router(autores.router)
app.include_router(categorias.router)
app.include_router(libros.router)
app.include_router(usuarios.router)
app.include_router(carrito.router)
app.include_router(pedidos.router)
app.include_router(valoraciones.router)
app.include_router(tarjetas.router)
app.include_router(registros.router)
app.include_router(autenticacion.router)

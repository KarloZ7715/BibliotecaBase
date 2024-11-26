from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/auth",
    tags=["autenticacion"],
)


@router.post("/registrar", response_model=schemas.Usuario)
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = (
        db.query(models.Usuario).filter(models.Usuario.correo == usuario.correo).first()
    )
    if db_usuario:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    nuevo_usuario = models.Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        contraseña=usuario.contraseña,
        direccion=usuario.direccion,
        telefono=usuario.telefono,
        rol="cliente",
        fecha_registro=datetime.now(),
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.post("/login", response_model=schemas.Usuario)
def login(
    form_data: schemas.Login,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    usuario = (
        db.query(models.Usuario)
        .filter(models.Usuario.correo == form_data.correo)
        .first()
    )
    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    if form_data.contraseña != usuario.contraseña:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    request.session["user_id"] = usuario.id_usuario
    return usuario


@router.post("/logout")
def logout(request: Request, response: Response):
    request.session.pop("user_id", None)
    return {"detail": "Desconectado exitosamente"}


@router.get("/me", response_model=schemas.Usuario)
def leer_usuario_actual(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="No autenticado")
    usuario = (
        db.query(models.Usuario).filter(models.Usuario.id_usuario == user_id).first()
    )
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

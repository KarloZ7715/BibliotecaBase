from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
)


@router.post("/", response_model=schemas.Usuario)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = (
        db.query(models.Usuario).filter(models.Usuario.correo == usuario.correo).first()
    )
    if db_usuario:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")
    db_usuario = models.Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        contraseña=usuario.contraseña,
        direccion=usuario.direccion,
        telefono=usuario.telefono,
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.get("/", response_model=List[schemas.Usuario])
def obtener_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(get_current_user),
):
    if usuario_actual.rol != "admin":
        raise HTTPException(
            status_code=403, detail="No tienes permiso para ver todos los usuarios"
        )
    usuarios = db.query(models.Usuario).offset(skip).limit(limit).all()
    return usuarios


@router.get("/{id_usuario}", response_model=schemas.Usuario)
def obtener_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(get_current_user),
):
    if usuario_actual.id_usuario != id_usuario and usuario_actual.rol != "admin":
        raise HTTPException(
            status_code=403, detail="No tienes permiso para ver este usuario"
        )
    usuario = (
        db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()
    )
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.put("/{id_usuario}", response_model=schemas.Usuario)
def actualizar_usuario(
    id_usuario: int,
    usuario: schemas.UsuarioCreate,
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(get_current_user),
):
    if usuario_actual.id_usuario != id_usuario and usuario_actual.rol != "admin":
        raise HTTPException(
            status_code=403, detail="No tienes permiso para actualizar este usuario"
        )
    db_usuario = (
        db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()
    )
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_usuario.nombre = usuario.nombre
    db_usuario.correo = usuario.correo
    db_usuario.contraseña = usuario.contraseña
    db_usuario.direccion = usuario.direccion
    db_usuario.telefono = usuario.telefono
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.delete("/{id_usuario}", response_model=schemas.Usuario)
def eliminar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(get_current_user),
):
    if usuario_actual.rol != "admin":
        raise HTTPException(
            status_code=403, detail="No tienes permiso para eliminar usuarios"
        )
    db_usuario = (
        db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()
    )
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(db_usuario)
    db.commit()
    return db_usuario

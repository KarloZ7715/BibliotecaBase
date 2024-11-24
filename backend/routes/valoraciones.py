from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/valoraciones",
    tags=["Valoraciones"],
)


@router.post("/", response_model=schemas.Valoracion)
def crear_valoracion(
    valoracion: schemas.ValoracionCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    if usuario.rol != "cliente":
        raise HTTPException(
            status_code=403, detail="Solo los clientes pueden crear valoraciones"
        )
    db_valoracion = models.Valoracion(
        **valoracion.dict(), id_usuario=usuario.id_usuario
    )
    db.add(db_valoracion)
    db.commit()
    db.refresh(db_valoracion)
    return db_valoracion


@router.get("/", response_model=List[schemas.Valoracion])
def obtener_valoraciones(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    valoraciones = db.query(models.Valoracion).offset(skip).limit(limit).all()
    return valoraciones


@router.get("/{id_valoracion}", response_model=schemas.Valoracion)
def obtener_valoracion(id_valoracion: int, db: Session = Depends(get_db)):
    valoracion = (
        db.query(models.Valoracion)
        .filter(models.Valoracion.id_valoracion == id_valoracion)
        .first()
    )
    if not valoracion:
        raise HTTPException(status_code=404, detail="Valoración no encontrada")
    return valoracion


@router.put("/{id_valoracion}", response_model=schemas.Valoracion)
def actualizar_valoracion(
    id_valoracion: int,
    valoracion: schemas.ValoracionCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    db_valoracion = (
        db.query(models.Valoracion)
        .filter(models.Valoracion.id_valoracion == id_valoracion)
        .first()
    )
    if not db_valoracion:
        raise HTTPException(status_code=404, detail="Valoración no encontrada")
    if db_valoracion.id_usuario != usuario.id_usuario and usuario.rol != "admin":
        raise HTTPException(
            status_code=403, detail="No tienes permiso para actualizar esta valoración"
        )
    db_valoracion.valoracion = valoracion.valoracion
    db.commit()
    db.refresh(db_valoracion)
    return db_valoracion


@router.delete("/{id_valoracion}", response_model=schemas.Valoracion)
def eliminar_valoracion(
    id_valoracion: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    db_valoracion = (
        db.query(models.Valoracion)
        .filter(models.Valoracion.id_valoracion == id_valoracion)
        .first()
    )
    if not db_valoracion:
        raise HTTPException(status_code=404, detail="Valoración no encontrada")
    if db_valoracion.id_usuario != usuario.id_usuario and usuario.rol != "admin":
        raise HTTPException(
            status_code=403, detail="No tienes permiso para eliminar esta valoración"
        )
    db.delete(db_valoracion)
    db.commit()
    return db_valoracion

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/tarjetas",
    tags=["Tarjetas"],
)


@router.post("/", response_model=schemas.Tarjeta)
def agregar_tarjeta(
    tarjeta: schemas.TarjetaCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    db_tarjeta = models.Tarjeta(**tarjeta.dict(), id_usuario=usuario.id_usuario)
    db.add(db_tarjeta)
    db.commit()
    db.refresh(db_tarjeta)
    return db_tarjeta


@router.get("/", response_model=List[schemas.Tarjeta])
def obtener_tarjetas(
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    tarjetas = (
        db.query(models.Tarjeta)
        .filter(models.Tarjeta.id_usuario == usuario.id_usuario)
        .all()
    )
    return tarjetas


@router.get("/{id_tarjeta}", response_model=schemas.Tarjeta)
def obtener_tarjeta(
    id_tarjeta: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    tarjeta = (
        db.query(models.Tarjeta)
        .filter(
            models.Tarjeta.id_tarjeta == id_tarjeta,
            models.Tarjeta.id_usuario == usuario.id_usuario,
        )
        .first()
    )
    if not tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return tarjeta


@router.put("/{id_tarjeta}", response_model=schemas.Tarjeta)
def actualizar_tarjeta(
    id_tarjeta: int,
    tarjeta: schemas.TarjetaCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    db_tarjeta = (
        db.query(models.Tarjeta)
        .filter(
            models.Tarjeta.id_tarjeta == id_tarjeta,
            models.Tarjeta.id_usuario == usuario.id_usuario,
        )
        .first()
    )
    if not db_tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    for key, value in tarjeta.dict().items():
        setattr(db_tarjeta, key, value)
    db.commit()
    db.refresh(db_tarjeta)
    return db_tarjeta


@router.delete("/{id_tarjeta}", response_model=schemas.Tarjeta)
def eliminar_tarjeta(
    id_tarjeta: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    db_tarjeta = (
        db.query(models.Tarjeta)
        .filter(
            models.Tarjeta.id_tarjeta == id_tarjeta,
            models.Tarjeta.id_usuario == usuario.id_usuario,
        )
        .first()
    )
    if not db_tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    db.delete(db_tarjeta)
    db.commit()
    return db_tarjeta
